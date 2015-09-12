from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^home_request_1/', views.home_request_1, name='home_request_1'),
    url(r'^home_request_2/', views.home_request_2, name='home_request_2'),
    url(r'^login_request/', views.login_request, name='login_request'),
    url(r'^commonly_popular_books', views.commonly_popular_books, name='commonly_popular_books'),
    url(r'^book_detail', views.book_detail, name='book_detail'),
    url(r'^related_books_request', views.related_books_request, name='related_books_request'),
    url(r'^categories_all_category', views.categories_all_category, name='categories_all_category'),
    url(r'^user_profile', views.user_profile, name='user_profile'),
    url(r'^recently_viewed_books', views.recently_viewed_books, name='recently_viewed_books'),
    url(r'^delete_recent_viewed_book', views.delete_recent_viewed_book, name='delete_recent_viewed_book'),
    url(r'^add_to_favourite', views.add_to_favourite, name='add_to_favourite'),
    url(r'^view_wishlist_request', views.view_wishlist_request, name='view_wishlist_request'),
    url(r'^autocomplete_search', views.autocomplete_search, name='autocomplete_search'),
    url(r'^logout_view', views.logout_view, name='logout_view'),
    url(r'^add_to_cart', views.add_to_cart, name='add_to_cart'),
    url(r'^remove_from_cart', views.remove_from_cart, name='remove_from_cart'),
    url(r'^view_cart_request', views.view_cart_request, name='view_cart_request'),
    url(r'^add_or_edit_address', views.add_or_edit_address, name='add_or_edit_address'),
]
