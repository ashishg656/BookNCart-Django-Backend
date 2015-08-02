from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^books/(?P<book_id>[0-9]+)/$', views.book_detail, name='book_detail'),
    url(r'^add_to_cart/', views.add_to_cart, name='add_to_cart'),
    url(r'^delete_from_cart/', views.delete_from_cart, name='delete_from_cart'),
    url(r'^facebook_login/', views.facebook_login, name='facebook_login'),
    url(r'^google_login/', views.google_login, name='google_login'),
    url(r'^sign_out/', views.sign_out, name='sign_out'),
]
