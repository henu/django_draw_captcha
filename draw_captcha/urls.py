from django.conf.urls import url

from . import views

app_name = 'draw_captcha'
urlpatterns = [
    url(r'^draw_captcha/get_details', views.get_details),
]
