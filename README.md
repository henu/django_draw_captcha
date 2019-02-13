The problem with captcha libraries is, that they are not able to generate new
content like humans. So I got this idea to write a captcha library for Django
that asks users to draw more material when needed. The actual captcha is to
choose correct objects from a 4 × 4 grid.

You can find a working demo from here: http://captcha.henu.fi/


How to use
==========

1. Install:

    ```
    pip install django-draw-captcha
    ```

2. Add to `settings.py`:

    ```
    INSTALLED_APPS = [
        'draw_captcha',
    ]
    ```

3 Add to `urls.py`:

    ```
    from django.conf.urls import url, include

    urlpatterns = [
        url(r'^', include('draw_captcha.urls')),
    ]
    ```

4. Use in code:

    ```
    from draw_captcha.forms import CaptchaField

    class SomeRandomForm(forms.Form):
        captcha = CaptchaField(label='')
    ```
