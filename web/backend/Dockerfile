# Builder #

FROM python:3.11.9-slim as builder

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y --no-install-recommends gcc

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /usr/src/app/wheels -r requirements.txt
RUN pip wheel --no-cache-dir --wheel-dir /usr/src/app/wheels python-dotenv

# Final #

FROM python:3.11.9-slim

RUN mkdir -p /home/app

RUN addgroup --system app && adduser --system --group app

ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
RUN mkdir $APP_HOME/mediafiles
WORKDIR $APP_HOME

ADD static $APP_HOME/staticfiles
ADD media $APP_HOME/mediafiles

RUN apt-get update && apt-get install -y --no-install-recommends netcat-traditional
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g'  $APP_HOME/entrypoint.sh
RUN chmod +x  $APP_HOME/entrypoint.sh

COPY . $APP_HOME

RUN chown -R app:app $APP_HOME
RUN chown -R app:app /usr/lib/

ENTRYPOINT ["/home/app/web/entrypoint.sh"]
