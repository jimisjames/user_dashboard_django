from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^reg$', views.reg),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^dashboard$', views.dashboard),
    url(r'^toggle/admin/(?P<id>\d+)$', views.toggle_admin),
    url(r'^wall/(?P<id>\d+)$', views.wall),
    url(r'^delete/(?P<id>\d+)$', views.delete),
    url(r'^message/(?P<id>\d+)$', views.message),
    url(r'^delete_message/(?P<message_id>\d+)/(?P<user_id>\d+)$', views.delete_message),
    url(r'^comment/(?P<id>\d+)$', views.comment),
    url(r'^delete_comment/(?P<comment_id>\d+)/(?P<user_id>\d+)$', views.delete_comment),
    url(r'^edit$', views.edit),
    url(r'^edit/(?P<user_id>\d+)$', views.edit),
    url(r'^form/None$', views.form),
    url(r'^form/(?P<user_id>\d+)$', views.form),

]
