from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^register$', views.index),
    url(r'^username$', views.username),
    url(r'^password$', views.password),
    url(r'^add_user$', views.register),
    url(r'^profile$', views.profile),
    url(r'^edit$', views.edit),
    url(r'^edit_profile$', views.edit_profile),
    url(r'^login_user$', views.login),
    url(r'^clear_reg$', views.clear_reg),
    url(r'^log_out$', views.log_out),
    url(r'^add_sheriff$', views.add_sheriff),
    url(r'^add_cowboy$', views.add_cowboy),
    url(r'^add_outlaw$', views.add_outlaw),
    url(r'^like/(?P<flavor_id>\d+)$', views.like),
    url(r'^unlike/(?P<flavor_id>\d+)$', views.unlike),
    url(r'^update_sub$', views.update_sub),
]