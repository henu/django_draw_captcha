How to use
==========

1. Add to `settings.py`:

    ```
    INSTALLED_APPS = [
        'draw_captcha',
    ]
    ```

2. Add to `urls.py`:

    ```
    from django.conf.urls import url, include

    urlpatterns = [
        url(r'^', include('draw_captcha.urls')),
    ]
    ```

3. Use in code:

    ```
    from draw_captcha.forms import CaptchaField

    class SomeRandomForm(forms.Form):
        captcha = CaptchaField(label='')
    ```
