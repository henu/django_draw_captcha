from django.conf.urls import url

from . import views

app_name = 'draw_captcha'
urlpatterns = [
    url(r'^draw_captcha/get_task', views.get_task),
    url(r'^draw_captcha/upload_drawing', views.upload_drawing),
    url(r'^draw_captcha/complete_task', views.complete_task),
]
