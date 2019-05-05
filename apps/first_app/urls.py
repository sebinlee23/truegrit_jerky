from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.main),
    url(r'^about$', views.about),
    url(r'^program$', views.program),
    url(r'^shop$', views.order),
    url(r'^add_cart$', views.add_cart),
    url(r'^update/(?P<product_name>[a-zA-Z\-]+)$', views.update),
    url(r'^delete/(?P<product_name>[a-zA-Z\-]+)$', views.delete),
    url(r'^cart$', views.cart),
]