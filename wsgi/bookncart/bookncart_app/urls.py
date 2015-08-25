from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^home_request_1/', views.home_request_1, name='home_request_1'),
    url(r'^home_request_2/', views.home_request_2, name='home_request_2'),
    url(r'^login_request/', views.login_request, name='login_request'),
]
