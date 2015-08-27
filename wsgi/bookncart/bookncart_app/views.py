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
        tags.append({'tag_name': tag.tag_name, 'id': tag.id})

    return JsonResponse({'latest_books': latest_books, 'top_rated_books': top_rated_books,
                         'currently_active_books': currently_active_books, 'tags': tags})


@csrf_exempt
def login_request(request):
    if request.method == 'POST':
        status = False
        user_id_to_send = None
        user_profile_id_to_send = None

        access_token = request.POST.get('access_token')
        user_id = request.POST.get('user_id')
        profile_object = request.POST.get('additional_data')
        email = request.POST.get('email')
        name = request.POST.get('name')
        image_url = request.POST.get('image_url')
        is_google_login = request.POST.get('is_google_login', False)

        is_google_login = parseBoolean(is_google_login)

        username = str(email) + str(user_id)
        password = user_id
        if len(username) > 30:
            username = username[0:29]

        user_profile = None
        user = authenticate(username=username, password=password)
        if user is not None:
            user_profile = UserProfiles.objects.get(user_link_obj=user)
            user_profile.access_token = access_token
            user_profile.profile_details_json_object = profile_object
            user_profile.profile_image = image_url
            user_profile.login_count += 1
            user_profile.is_logged_in = True
            user_profile.save()
            login(request, user)
            status = True
            user_profile_id_to_send = user_profile.id
            user_id_to_send = user.id
        else:
            user = User.objects.create_user(username, str(email), password)
            user.first_name = str(name)
            user.last_name = ""
            user.save()
            user_profile = UserProfiles(user_link_obj=user)
            user_profile.full_name = name
            user_profile.first_name = name
            user_profile.middle_name = ""
            user_profile.last_name = ""
            user_profile.email = email
            user_profile.password = password
            user_profile.username = username
            user_profile.userIDAuth = user_id
            user_profile.is_google_account = is_google_login
            user_profile.access_token = access_token
            user_profile.profile_details_json_object = profile_object
            user_profile.profile_image = image_url
            user_profile.login_count = 1
            user_profile.is_logged_in = True
            user_profile.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                status = True
                user_profile_id_to_send = user_profile.id
                user_id_to_send = user.id
        if user_profile is not None:
            try:
                location = Location(user_id=user_profile)
                location.http_get_host = request.get_host()
                location.http_host = request.META['HTTP_HOST']
                location.http_referer = request.META['HTTP_REFERER']
                location.http_user_agent = request.META['HTTP_USER_AGENT']
                try:
                    location.remote_host = request.META['REMOTE_ADDR']
                    location.remote_addr = request.META['REMOTE_HOST']
                except:
                    pass
                try:
                    location.remote_user = request.META['REMOTE_USER']
                except:
                    pass
                location.save()
            except:
                pass
        return JsonResponse({"status": status, "user_profile_id": user_profile_id_to_send, "user_id": user_id_to_send})


@csrf_exempt
def sample_request(request):
    if request.method == 'POST':
        booleans = request.POST.get('boolean')
        strings = request.POST.get('string')
        intehe = request.POST.get('integer')

        return JsonResponse({"booleans": booleans, "strings": strings, "integer": intehe})


def parseBoolean(stringToParse):
    if stringToParse == 'True' or stringToParse == "true" or stringToParse == 1 or stringToParse == True or stringToParse == 'TRUE':
        return True
    return False
