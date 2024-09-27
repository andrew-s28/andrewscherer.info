from datetime import datetime
import os

from dotenv import load_dotenv, find_dotenv
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count
from django.http import JsonResponse
from django.utils import timezone
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from bokeh.plotting import ColumnDataSource, figure
from bokeh.embed import components
from bokeh.models import CustomJS, DateRangePicker, InlineStyleSheet
import pandas as pd
from sqlalchemy import create_engine

from .models import BlogPost, UploadedImages

# Create your views here.


class BlogView(generic.ListView):
    paginate_by = 5
    model = BlogPost
    template_name = 'blog/blog.html'
    context_object_name = 'blogs'

    def get_queryset(self):
        return BlogPost.objects.filter(
            pub_date__lte=timezone.now()
        ).filter(
            visible=True
        ).order_by('-pub_date')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_posts'] = get_recent_posts(BlogPost)
        context['popular_tags'] = get_popular_tags(BlogPost)
        return context


class DateView(generic.ListView):
    paginate_by = 5
    model = BlogPost
    template_name = 'blog/date.html'
    context_object_name = 'blogs'

    def get_queryset(self):
        year, month = self.kwargs['date'].split('-')
        return BlogPost.objects.filter(
            pub_date__year=year, pub_date__month=month
        ).filter(
            pub_date__lte=timezone.now()
        ).filter(
            visible=True
        ).order_by('-pub_date')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_posts'] = get_recent_posts(BlogPost)
        context['popular_tags'] = get_popular_tags(BlogPost)
        current_date = datetime.strptime(self.kwargs['date'], '%Y-%m')
        context['current_date'] = current_date.strftime('%B %Y')
        return context


class TagView(generic.ListView):
    paginate_by = 5
    model = BlogPost
    template_name = 'blog/tag.html'
    context_object_name = 'blogs'

    def get_queryset(self):
        return BlogPost.objects.filter(
            tags__name=self.kwargs['tag']
        ).filter(
            pub_date__lte=timezone.now()
        ).filter(
            visible=True
        ).order_by('-pub_date')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_posts'] = get_recent_posts(BlogPost)
        context['popular_tags'] = get_popular_tags(BlogPost)
        context['current_tag'] = self.kwargs['tag']
        return context


class ArticleView(generic.DetailView):
    model = BlogPost
    template_name = 'blog/article.html'
    context_object_name = 'article'

    def get_queryset(self):
        return BlogPost.objects.filter(
            pub_date__lte=timezone.now()
        ).filter(
            visible=True
        ).order_by('-pub_date')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_posts'] = get_recent_posts(BlogPost)
        context['popular_tags'] = get_popular_tags(BlogPost)
        if context['object'].title == 'Pollen Tracker':
            context['script'], context['div'] = allergen_plot()
        return context


def get_popular_tags(BlogPost: BlogPost):
    return BlogPost.tags.most_common().filter(
        id__in=BlogPost.objects.filter(pub_date__lte=timezone.now()).filter(visible=True).order_by('-pub_date').values('tags')
    )[:5]


def get_recent_posts(BlogPost: BlogPost):
    return BlogPost.objects.filter(
        pub_date__lte=timezone.now()
    ).filter(
        visible=True
    ).order_by('-pub_date')[:5]


@csrf_exempt
@user_passes_test(lambda u: u.is_superuser)
def upload_image(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Wrong request'}, status=400)

    file = request.FILES['file']
    file_suffix = file.name.split('.')[-1]
    if file_suffix not in ['jpg', 'jpeg', 'png', 'gif']:
        return JsonResponse({'error': f'Wrong image format {file_suffix}'}, status=400)

    file_path = os.path.join(settings.MEDIA_ROOT, 'tinymce/')

    if not os.path.exists(file_path):
        os.makedirs(file_path)
    file_name = file.name.split('.')[0]
    file_path = os.path.join(file_path, file_name + '.' + file_suffix)
    file_url = settings.MEDIA_URL + 'tinymce/' + os.path.basename(file_name + '.' + file_suffix)
    if os.path.exists(file_path):
        return JsonResponse({'error': f'File {file_name} already exists'}, status=400)

    with open(file_path, 'wb+') as f:
        for chunk in file.chunks():
            f.write(chunk)
        UploadedImages.objects.get_or_create(image='tinymce/' + os.path.basename(file_path))
        return JsonResponse({
            'message': 'Image uploaded successfully',
            'location': file_url,
        })


def allergen_plot():
    load_dotenv(find_dotenv())
    db_name = os.getenv('DB_NAME')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_url = 'postgresql+psycopg2://' + db_user + ':' + db_password + '@' + db_host + ':' + db_port + '/' + db_name
    engine = create_engine(
        db_url,
    )
    df: pd.DataFrame = pd.read_sql_table('allergen_data', engine, parse_dates=['true_date'])
    df.where(df['true_date'] > '2024-04-01', inplace=True)
    df.dropna(inplace=True)
    source = ColumnDataSource(df)
    plot = figure(
        sizing_mode='stretch_width',
        max_height=450,
        title='Allergen Data from Oregon Allergy Associates, Eugene, OR',
        y_axis_label='Pollen Count',
        x_axis_type="datetime"
    )
    plot.line(
        x='true_date',
        y='grass_pollen',
        source=source,
        line_width=2,
        color='green',
        legend_label='Grass Pollen'
    )
    plot.line(
        x='true_date',
        y='tree_pollen',
        source=source,
        line_width=2,
        color='red',
        legend_label='Tree Pollen'
    )
    stylesheet = InlineStyleSheet(css=".bk-input { background-color: transparent !important; }")
    picker = DateRangePicker(
        title='Select date range',
        value=(df['true_date'].min().date(), df['true_date'].max().date()),
        min_date=df['true_date'].min().date(),
        max_date=df['true_date'].max().date(),
        stylesheets=[stylesheet]
    )
    picker.js_on_change(
        'value',
        CustomJS(
            args=dict(x_range=plot.x_range, y_range=plot.y_range, source=source),
            code="""
            var start = Date.parse(this.value[0]);
            var end = Date.parse(this.value[1]);
            x_range.start = start;
            x_range.end = end;
            var start_index = source.data['true_date'].findIndex((date) => date >= start);
            var end_index = source.data['true_date'].findIndex((date) => date >= end);
            var grass_max = Math.max(...source.data['grass_pollen'].slice(start_index, end_index));
            var tree_max = Math.max(...source.data['tree_pollen'].slice(start_index, end_index));
            y_range.start = -10;
            if (grass_max > tree_max) {
                y_range.end = grass_max + 50;
            } else {
                y_range.end = tree_max + 50;
            }
            """)
    )
    script, (div1, div2) = components((plot, picker))
    script += '<script src="https://cdn.bokeh.org/bokeh/release/bokeh-3.4.1.min.js" crossorigin="anonymous"></script>'
    script += '<script src="https://cdn.bokeh.org/bokeh/release/bokeh-widgets-3.4.1.min.js" crossorigin="anonymous"></script>'
    return script, div2 + div1
