from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^signin/$', views.signin, name="signin"),
    url(r'^signup/save_image', views.save_image, name='signup_save_image'),
    url(r'^signin/save_image', views.save_image, name='signin_save_image')
]