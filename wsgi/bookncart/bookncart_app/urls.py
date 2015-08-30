from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^home_request_1/', views.home_request_1, name='home_request_1'),
    url(r'^home_request_2/', views.home_request_2, name='home_request_2'),
    url(r'^login_request/', views.login_request, name='login_request'),
    url(r'^commonly_popular_books', views.commonly_popular_books, name='commonly_popular_books'),
    url(r'^book_detail', views.book_detail, name='book_detail'),
]
