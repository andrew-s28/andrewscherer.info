/*!
 * Adapted from the original by Andrew Scherer:
 * Color mode toggler for Bootstrap's docs (https://getbootstrap.com/)
 * Copyright 2011-2024 The Bootstrap Authors
 * Licensed under the Creative Commons Attribution 3.0 Unported License.
 */

(() => {
    'use strict'   

    const setActivePage = () => {
      var currentDir = document.URL.split('/').slice(3, 4).join('/');
      var navbarPages = document.querySelectorAll('.nav-page');
      navbarPages.forEach(page => {
        page.classList.remove('active');
        if (currentDir == page.id) {
          page.classList.add('active');
        } else if (page.id == 'home' && currentDir == '') {
          page.classList.add('active');
        }
      });
    }

    const setNavbarTheme = theme => {
      var navbarPages = document.querySelectorAll('.nav-page');
      navbarPages.forEach(page => {
        page.classList.remove('dark');
        page.classList.remove('light');
        page.classList.remove('auto');
        if (theme == 'dark') {
          page.classList.add('dark');
        } else if (theme == 'light') {
          page.classList.add('light');
        } else if (theme == 'auto') {
          var preferredTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
          page.classList.add(preferredTheme);
        }
      });
    }


    const getStoredTheme = () => localStorage.getItem('theme')
    const setStoredTheme = theme => localStorage.setItem('theme', theme)
  
    const getPreferredTheme = () => {
      const storedTheme = getStoredTheme()
      if (storedTheme) {
        return storedTheme
      }
  
      return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
    }
  
    const setTheme = theme => {
      if (theme === 'auto') {
        document.documentElement.setAttribute('data-bs-theme', (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'))
      } else {
        document.documentElement.setAttribute('data-bs-theme', theme)
      }
    }
  
    setTheme(getPreferredTheme())
  
    const showActiveTheme = (theme) => {
      const themeSwitcher = document.querySelector('.bd-theme');
  
      if (!themeSwitcher) {
        return
      }
  
      const themeSwitcherText = document.querySelector('#bd-theme-text');
      const btnToActive = document.querySelector(`[data-bs-theme-value="${theme}"]`);

      document.querySelectorAll('[data-bs-theme-value]').forEach(element => {
        element.classList.remove('active')
        element.setAttribute('aria-pressed', 'false')
      });
  
      btnToActive.classList.add('active');
      btnToActive.setAttribute('aria-pressed', 'true');
      const themeSwitcherLabel = `${themeSwitcherText.textContent} (current theme: ${btnToActive.dataset.bsThemeValue})`;
      themeSwitcher.setAttribute('aria-label', themeSwitcherLabel);

      const images = document.querySelectorAll('.bd-image-theme');
      const dividers = document.querySelectorAll('.theme-divider');

      images.forEach(image => {
        if (theme === 'auto') {
          const theme_preferred = (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
          image.src = image.src.replace(/[^\/]+$/, `circle-half-${theme_preferred}.svg`);
        } else if (theme === 'light') {
          image.src = image.src.replace(/[^\/]+$/, `sun-fill-${theme}.svg`);
        } else if (theme === 'dark') {
          image.src = image.src.replace(/[^\/]+$/, `moon-stars-fill-${theme}.svg`);
        }
      });
      dividers.forEach(divider => {
        divider.classList.remove('text-white', 'text-black');
        if (theme === 'auto') {
          const theme_preferred = (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
          if (theme_preferred === 'dark') {
            divider.classList.add('text-white');
          } else if (theme_preferred === 'light') {
           divider.classList.add('text-black');
          }
        } else if (theme === 'light') {
          divider.classList.add('text-black');
        } else if (theme === 'dark') {
          divider.classList.add('text-white');
        }
      });
    }

    const setThemeDropdown = (theme) => {
      const images = document.querySelectorAll('.bd-image-theme-dropdown')
      images.forEach(image => {
        if (theme == 'auto') {
          theme = (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light')
        }
        if (image.getAttribute('alt') === 'Light Mode') {
          image.src = image.src.replace(/[^\/]+$/, `sun-fill-${theme}.svg`)
        } else if (image.getAttribute('alt') === 'Dark Mode') {
          image.src = image.src.replace(/[^\/]+$/, `moon-stars-fill-${theme}.svg`)
        } else if (image.getAttribute('alt') === 'Auto Light/Dark Mode') {
          image.src = image.src.replace(/[^\/]+$/, `circle-half-${theme}.svg`)
        }
      })
    }

    const themeRegex = (theme) => {
      if (theme === 'auto') {
        theme = (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light')
      }
      if (theme == 'light') {
        return new RegExp(`-dark`)
      } else if (theme == 'dark') {
        return new RegExp(`-light`)
      }
    }

    const showActiveImage = (theme) => {
      const images = document.querySelectorAll('.bd-image');
      if (theme === 'auto') {
        theme = (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
      }
      images.forEach(image => {
        image.src = image.src.replace(themeRegex(theme), `-${theme}`);
      })
    }
  
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
      const storedTheme = getStoredTheme()
      if (storedTheme !== 'light' && storedTheme !== 'dark') {
        setTheme(getPreferredTheme())
      }
    })
  
    window.addEventListener('DOMContentLoaded', () => {
      setActivePage();
      // set theme initially on page load
      if (!getStoredTheme()) {
        setStoredTheme(getPreferredTheme());
      }
      const theme = getStoredTheme();
      setStoredTheme(theme);
      setTheme(theme);
      showActiveTheme(theme);
      showActiveImage(theme);
      setThemeDropdown(theme);
      setNavbarTheme(theme);
      // set theme again whenever a new theme is selected in dropdown
      document.querySelectorAll('[data-bs-theme-value]')
        .forEach(toggle => {
          toggle.addEventListener('click', () => {
            const theme = toggle.getAttribute('data-bs-theme-value');
            setStoredTheme(theme);
            setTheme(theme);
            showActiveTheme(theme);
            showActiveImage(theme);
            setThemeDropdown(theme);
            setNavbarTheme(theme);
          });
        });
    });
  })()
