from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^books/(?P<book_id>[0-9]+)/$', views.book_detail, name='book_detail'),
    url(r'^add_to_cart/' , views.add_to_cart, name='add_to_cart'),
]
