from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^order_confirm$', views.order_confirm),
    url(r'^confirmation$', views.confirmation),
    url(r'^show_order/(?P<order_id>\d+)$', views.show_order),
]