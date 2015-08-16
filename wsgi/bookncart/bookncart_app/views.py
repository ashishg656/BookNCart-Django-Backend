from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpRequest, Http404, JsonResponse
from django.shortcuts import render, redirect
from PIL import Image
from django.template import RequestContext
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.core import serializers
import json
import requests
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from bookncart_web.models import *
from django.core import serializers


def home_request_1(request):
    banners_model = Banners.objects.filter(active=True).order_by('-upload_date')
    banners = []
    for banner in banners_model:
        banners.append({'banner_image': banner.banner_image.url, })

    categories_model = Categories.objects.filter(is_root=False, is_last=False)
    categories = []
    for category in categories_model:
        categories.append({'name': category.name, 'id': category.id, 'image_url': category.image_url.url,
                           'image_url_2': category.image_url_2.url})

    featured_books_model = Books.objects.filter(stock__gt=0, is_featured__exact=1).order_by('-view_count')[:10]
    featured_books = []
    for book in featured_books_model:
        featured_books.append({'name': book.name, 'price': book.price, 'image_url': book.image_url.url, 'id': book.id})

    best_selling_books_model = Books.objects.filter(stock__gt=0, ).order_by('-sell_count')[:10]
    best_selling_books = []
    for book in best_selling_books_model:
        best_selling_books.append(
            {'name': book.name, 'price': book.price, 'image_url': book.image_url.url, 'id': book.id})

    return JsonResponse({'banners': banners, 'categories': categories, 'featured_books': featured_books,
                         'best_selling_books': best_selling_books})


def home_request_2(request):
    latest_books_model = Books.objects.filter(stock__gt=0).order_by('-upload_date')[:10]
    latest_books = []
    for book in latest_books_model:
        latest_books.append(
            {'name': book.name, 'price': book.price, 'image_url': book.image_url.url, 'id': book.id})

    top_rated_books_model = Books.objects.filter(stock__gt=0).order_by('-view_count')[:10]
    top_rated_books = []
    for book in top_rated_books_model:
        top_rated_books.append(
            {'name': book.name, 'price': book.price, 'image_url': book.image_url.url, 'id': book.id})

    currently_active_books_model = Books.objects.filter(stock__gt=0).order_by('-last_active_time')[:10]
    currently_active_books = []
    for book in currently_active_books_model:
        currently_active_books.append(
            {'name': book.name, 'price': book.price, 'image_url': book.image_url.url, 'id': book.id})

    tags_model = Tags.objects.all()[:20]
    tags = []
    for tag in tags_model:
        tags.append({'tag_name': tag.tag_name,'id':tag.id})

    return JsonResponse({'latest_books': latest_books, 'top_rated_books': top_rated_books,
                         'currently_active_books': currently_active_books, 'tags': tags})
