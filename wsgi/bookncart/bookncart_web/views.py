from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse
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


def index(request):
    # try:
    # del request.session['cart_items']
    best_selling_books = Books.objects.filter(stock__gt=0).order_by('-sell_count')[:30]
    top_rated_books = Books.objects.filter(stock__gt=0).order_by('-view_count')[:30]
    featured_books = Books.objects.filter(stock__gt=0).filter(is_featured__exact=1).order_by('-view_count')[:30]
    new_added_books = Books.objects.filter(stock__gt=0).order_by('-upload_date')[:30]
    context = RequestContext(request, {
        'best_selling_books': best_selling_books,
        'top_rated_books': top_rated_books,
        'featured_books': featured_books,
        'new_added_books': new_added_books
    }, [view_for_requestcontext_data_common_view])
    return render(request, 'bookncart_web/index.html', context)
    # except:
    #     raise Http404('Internal error occurred in index view')


def book_detail(request, book_id):
    try:
        book = get_object_or_404(Books, pk=book_id)
        book.view_count += 1
        book.save()
        related_books = []
        tags = book.tags_id.all()
        for tag in tags:
            temp_books = tag.books_set.all()
            for temp_book in temp_books:
                if temp_book.id != book.id and temp_book.stock > 0:
                    related_books.append(temp_book)
        related_books = set(related_books)
        reviews = Reviews.objects.filter(book_id__exact=book_id).filter(is_approved__exact=1).order_by('-timestamp')

        context = RequestContext(request, {
            'book': book,
            'related_books': related_books,
            'reviews': reviews
        }, [view_for_requestcontext_data_common_view])
        return render(request, 'bookncart_web/book_detail.html', context)
    except:
        raise Http404('Internal error occurred in book_detail view')


def add_to_favourites(request):
    # if request
    pass


@csrf_exempt
def delete_from_cart(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        book_cart = get_object_or_404(Books, pk=book_id)
        try:
            new_cart_items = []
            cart_items = request.session['cart_items']
            for cart_item in cart_items:
                if cart_item['id'] == book_cart.id:
                    pass
                else:
                    new_cart_items.append(cart_item)

            request.session['cart_items'] = new_cart_items

            cart_items = new_cart_items
            subtotal = 0
            quantity = 0
            for cart_item in cart_items:
                subtotal += cart_item['amount']
                quantity += cart_item['quantity']
            total = subtotal + 50
            if subtotal == 0:
                total = 0

            request.session['cart_subtotal'] = subtotal
            request.session['cart_total'] = total
            request.session['cart_quantity'] = quantity

            return JsonResponse({'cart_items': cart_items, 'subtotal': subtotal, 'quantity': quantity, 'total': total,
                                 'message_type': 'delete'})
        except:
            return Http404


@csrf_exempt
def add_to_cart(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        book_cart = get_object_or_404(Books, pk=book_id)
        cart_items = []
        error_message = None
        try:
            cart_items = request.session['cart_items']
        except:
            cart_items = []
        if len(cart_items) > 0:
            found = False
            for cart_item in cart_items:
                if cart_item['id'] == book_cart.id:
                    if cart_item['quantity'] < 10:
                        cart_item['quantity'] += 1
                        cart_item['amount'] = cart_item['price'] * cart_item['quantity']
                    else:
                        error_message = "You cannot add more than 10 items of " + book_cart.name;
                    found = True
            if found == False:
                cart_items.append(
                    {'name': book_cart.name, 'id': book_cart.id, 'price': book_cart.price, 'quantity': 1,
                     'image_url': book_cart.image_url.url, 'amount': book_cart.price})
        else:
            cart_items.append(
                {'name': book_cart.name, 'id': book_cart.id, 'price': book_cart.price, 'quantity': 1,
                 'image_url': book_cart.image_url.url, 'amount': book_cart.price})

        request.session['cart_items'] = cart_items

        subtotal = 0
        quantity = 0
        for cart_item in cart_items:
            subtotal += cart_item['amount']
            quantity += cart_item['quantity']
        total = subtotal + 50

        request.session['cart_subtotal'] = subtotal
        request.session['cart_total'] = total
        request.session['cart_quantity'] = quantity

        return JsonResponse({'cart_items': cart_items, 'subtotal': subtotal, 'quantity': quantity, 'total': total,
                             'error_message': error_message, 'message_type': 'add'})


def view_for_requestcontext_data_common_view(request):
    top_category = Categories.objects.filter(is_root__exact=1)
    sub_category = Categories.objects.filter(is_root__exact=0).filter(is_last__exact=0)
    subsub_category = Categories.objects.filter(is_last__exact=1)
    cart_items = []
    cart_subtotal = 0
    cart_total = 0
    cart_quantity = 0
    try:
        cart_items = request.session['cart_items']
        cart_subtotal = request.session['cart_subtotal']
        cart_total = request.session['cart_total']
        cart_quantity = request.session['cart_quantity']
    except:
        cart_items = []
    context = {'top_category': top_category,
               'sub_category': sub_category,
               'subsub_category': subsub_category,
               'cart_items': cart_items,
               'cart_total': cart_total,
               'cart_subtotal': cart_subtotal,
               'cart_quantity': cart_quantity}
    return context


@csrf_exempt
def facebook_login(request):
    if request.method == 'POST':
        access_token = request.POST.get('access_token')
        expires_in = request.POST.get('expires_in')
        granted_scopes = request.POST.get('granted_scopes')
        signed_request = request.POST.get('signed_request')
        user_id = request.POST.get('user_id')
        profile_object = request.POST.get('profile_object')
        print(profile_object)
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name')
        last_name = request.POST.get('last_name')
        name = request.POST.get('name')
        image_url = request.POST.get('image_url')
        url = 'https://graph.facebook.com/v2.4/oauth/access_token?grant_type=fb_exchange_token'
        url += '&client_id=509658639190611&client_secret=4201c4b846d3be4a17998568e5b9fe44&fb_exchange_token='
        url += str(access_token)
        access_token_request = requests.get(url)
        long_live_access_token_fb = access_token_request.json()['access_token']
        long_live_access_token_fb_expires_in = access_token_request.json()['expires_in']

        username = str(email) + str(user_id)
        password = user_id
        if len(username) > 30:
            username = username[0:29]

        print(username)
        print(password)
        user = authenticate(username=username, password=password)
        if user is not None:
            user_profile = UserProfiles.objects.get(user_link_obj=user)
            user_profile.access_token = access_token
            user_profile.long_live_access_token = long_live_access_token_fb
            user_profile.access_token_expires_in = expires_in
            user_profile.long_live_access_token_expires_in = long_live_access_token_fb_expires_in
            user_profile.granted_scopes = str(granted_scopes)
            user_profile.signed_request = signed_request
            user_profile.profile_details_json_object = profile_object
            user_profile.profile_image = image_url
            user_profile.login_count += 1
            user_profile.is_logged_in = True
            user_profile.save()
            login(request, user)
        else:
            user = User.objects.create_user(username, str(email), password)
            if first_name is not None:
                user.first_name = str(first_name)
            if last_name is not None:
                user.last_name = str(last_name)
            user.save()
            user_profile = UserProfiles(user_link_obj=user)
            user_profile.full_name = name
            user_profile.first_name = first_name
            user_profile.middle_name = middle_name
            user_profile.last_name = last_name
            user_profile.email = email
            user_profile.password = password
            user_profile.username = username
            user_profile.userIDAuth = user_id
            user_profile.is_google_account = False
            user_profile.access_token = access_token
            user_profile.long_live_access_token = long_live_access_token_fb
            user_profile.access_token_expires_in = expires_in
            user_profile.long_live_access_token_expires_in = long_live_access_token_fb_expires_in
            user_profile.granted_scopes = str(granted_scopes)
            user_profile.signed_request = signed_request
            user_profile.profile_details_json_object = profile_object
            user_profile.profile_image = image_url
            user_profile.login_count = 1
            user_profile.is_logged_in = True
            user_profile.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
        return HttpResponse()


@csrf_exempt
def sign_out(request):
    if request.user.is_authenticated():
        user_profile = UserProfiles.objects.get(user_link_obj=request.user)
        user_profile.is_logged_in = False
        user_profile.save()
    logout(request)
    return HttpResponse()
