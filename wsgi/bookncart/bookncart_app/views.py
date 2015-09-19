from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpRequest, Http404, JsonResponse
from django.shortcuts import render, redirect
from PIL import Image
from django.template import RequestContext
from django.template.context_processors import request
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.core import serializers
import json
import requests
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from bookncart_web.models import *
from django.core import serializers
from push_notifications.models import GCMDevice

# 0 - featured books
# 1 - best selling books
# 2 - latest books
# 3 - top rated books
# 4 - currently active books
# 6 - category
# 7 - tags

delivery_charge_normal_constant = 50
delivery_free_minimum_constant = 1000


@csrf_exempt
def commonly_popular_books(request):
    user_id = request.POST.get('user_id', None)
    user_profile_id = request.POST.get('user_profile_id', None)
    device_id = request.POST.get('device_id', None)
    mode = request.POST.get("mode", 0)
    mode = int(mode)
    category_id = request.POST.get('category_id', None)
    pagenumber = request.POST.get("pagenumber", 1)
    pagesize = request.POST.get("pagesize", 10)
    tag_id = request.POST.get('tag_id', None)

    books_model_to_fetch = []

    if mode == 0:
        books_model_to_fetch = Books.objects.filter(stock__gt=0, is_featured__exact=1).order_by('-view_count')
    elif mode == 1:
        books_model_to_fetch = Books.objects.filter(stock__gt=0, ).order_by('-sell_count')
    elif mode == 2:
        books_model_to_fetch = Books.objects.filter(stock__gt=0).order_by('-upload_date')
    elif mode == 3:
        books_model_to_fetch = Books.objects.filter(stock__gt=0).order_by('-view_count')
    elif mode == 4:
        books_model_to_fetch = Books.objects.filter(stock__gt=0).order_by('-last_active_time')
    elif mode == 6:
        books_model_to_fetch = Books.objects.filter(stock__gt=0, categories_id=category_id).order_by('-view_count')
    elif mode == 7:
        books_model_to_fetch = Books.objects.filter(stock__gt=0, tags_id__exact=tag_id).order_by('-view_count')

    books_paginated = Paginator(books_model_to_fetch, pagesize)
    books_model_to_fetch = books_paginated.page(pagenumber)

    books_array = []
    for book in books_model_to_fetch:
        is_favourite = False
        if user_profile_id is not None:
            try:
                query = User_wishlist.objects.get(is_active=True, user_id_id__exact=int(user_profile_id),
                                                  book_id_id__exact=book.id)
                is_favourite = True
            except:
                is_favourite = False
        books_array.append({'name': book.name, 'price': book.price, 'image_url': book.image_url.url, 'id': book.id,
                            'is_favourite': is_favourite})

    next_page = None
    if books_model_to_fetch.has_next():
        next_page = books_model_to_fetch.next_page_number()

    return JsonResponse(
        {'books': books_array, 'next_page': next_page})


@csrf_exempt
def add_to_favourite(request):
    user_id = request.POST.get('user_id', None)
    user_profile_id = request.POST.get('user_profile_id', None)
    device_id = request.POST.get('device_id', None)
    book_id = request.POST.get('book_id')
    askForNumberOfLikesOnBook = request.POST.get('askForNumberOfLikesOnBook', False)
    askForNumberOfLikesOnBook = parseBoolean(askForNumberOfLikesOnBook)

    book = get_object_or_404(Books, pk=int(book_id))

    error = True
    removedFromFavourites = False

    if user_profile_id is not None:
        try:
            wishlist_books_model = User_wishlist.objects.get(user_id_id__exact=int(user_profile_id),
                                                             book_id_id__exact=book.id)
            if wishlist_books_model.is_active == True:
                wishlist_books_model.is_active = False
                wishlist_books_model.save()
                removedFromFavourites = True
                error = False
            else:
                wishlist_books_model.is_active = True
                wishlist_books_model.save()
                error = False
        except:
            wishlist_books_model = User_wishlist(is_active=True, book_id=book)
            user_profile = UserProfiles.objects.get(pk=int(user_profile_id))
            wishlist_books_model.user_id = user_profile
            wishlist_books_model.save()
            error = False

    wishlist_count = 0
    try:
        wishlist_count = User_wishlist.objects.filter(is_active=True, user_id_id__exact=int(
            user_profile_id)).count()
    except:
        wishlist_count = 0

    numberOfLikesOnBook = None
    if askForNumberOfLikesOnBook:
        numberOfLikesOnBook = User_wishlist.objects.filter(book_id__exact=int(book_id), is_active=True).count()

    return JsonResponse(
        {'error': error, 'removedFromFavourites': removedFromFavourites, 'wishlist_count': wishlist_count,
         'numberOfLikesOnBook': numberOfLikesOnBook})


@csrf_exempt
def add_to_cart(request):
    user_profile_id = request.POST.get('user_profile_id', None)
    device_id = request.POST.get('device_id', None)
    book_id = request.POST.get('book_id')
    quantity = request.POST.get('quantity', None)

    if quantity is not None:
        quantity = int(quantity)
        if quantity > 10:
            quantity = 10
    book = get_object_or_404(Books, pk=int(book_id))

    error = False
    isAlreadyTen = False
    errorMessage = None
    cart_count = 0

    books_model_to_fetch = []
    if user_profile_id is not None:
        try:
            cart_books_model = User_cart.objects.get(user_id_id__exact=int(user_profile_id),
                                                     book_id_id__exact=book.id)
            books_model_to_fetch = User_cart.objects.filter(is_active=True, user_id_id__exact=int(
                user_profile_id))
            if cart_books_model.is_active:
                if quantity is not None:
                    cart_books_model.quantity = quantity
                    cart_books_model.save()
                else:
                    if cart_books_model.quantity < 10:
                        cart_books_model.quantity += 1
                        cart_books_model.save()
                    else:
                        isAlreadyTen = True
                        error = True
                        errorMessage = "Sorry.Cannot add more than 10 items of the same book."
                        cart_books_model.quantity = 10
                        cart_books_model.save()
            else:
                cart_books_model.is_active = True
                if quantity is None:
                    cart_books_model.quantity = 1
                else:
                    cart_books_model.quantity = quantity
                cart_books_model.save()
        except:
            cart_instance = User_cart(is_active=True, book_id=book)
            if quantity is None:
                cart_instance.quantity = 1
            else:
                cart_instance.quantity = quantity
            user_profile = get_object_or_404(UserProfiles, pk=int(user_profile_id))
            cart_instance.user_id = user_profile
            cart_instance.save()
        cart_count = User_cart.objects.filter(is_active=True, user_id_id__exact=int(user_profile_id)).count()

    elif device_id is not None:
        try:
            cart_books_model = User_cart.objects.get(device_id__exact=int(device_id),
                                                     book_id_id__exact=book.id)
            books_model_to_fetch = User_cart.objects.filter(is_active=True, device_id__exact=int(device_id))
            if cart_books_model.is_active:
                if quantity is not None:
                    cart_books_model.quantity = quantity
                    cart_books_model.save()
                else:
                    if cart_books_model.quantity < 10:
                        cart_books_model.quantity += 1
                        cart_books_model.save()
                    else:
                        isAlreadyTen = True
                        error = True
                        errorMessage = "Sorry.Cannot add more than 10 items of the same book."
                        cart_books_model.quantity = 10
                        cart_books_model.save()
            else:
                cart_books_model.is_active = True
                if quantity is None:
                    cart_books_model.quantity = 1
                else:
                    cart_books_model.quantity = quantity
                cart_books_model.save()
        except:
            cart_instance = User_cart(is_active=True, book_id=book)
            if quantity is None:
                cart_instance.quantity = 1
            else:
                cart_instance.quantity = quantity
            cart_instance.device_id = device_id
            cart_instance.save()
        cart_count = User_cart.objects.filter(is_active=True, device_id__exact=int(device_id)).count()

    total_quantity = 0
    cart_total = 0

    for book_recent in books_model_to_fetch:
        if book_recent.book_id.stock > 0:
            total_quantity += 1
            cart_total += (book_recent.book_id.price * book_recent.quantity)

    if cart_total > delivery_free_minimum_constant:
        delivery_charge = 0
    else:
        delivery_charge = delivery_charge_normal_constant
    total_amount = cart_total + delivery_charge

    return JsonResponse(
        {'error': error, 'errorMessage': errorMessage, 'isAlreadyTen': isAlreadyTen, 'cart_count': cart_count,
         'total_quantity': total_quantity, 'cart_total': cart_total, 'delivery_charge': delivery_charge,
         'total_amount': total_amount})


@csrf_exempt
def remove_from_cart(request):
    user_profile_id = request.POST.get('user_profile_id', None)
    device_id = request.POST.get('device_id', None)
    book_id = request.POST.get('book_id')

    error = False
    errorMessage = None
    cart_count = 0

    books_model_to_fetch = []
    if user_profile_id is not None:
        try:
            cart_books_model = User_cart.objects.get(user_id_id__exact=int(user_profile_id),
                                                     book_id_id__exact=int(book_id))
            books_model_to_fetch = User_cart.objects.filter(is_active=True, user_id_id__exact=int(
                user_profile_id))
            if cart_books_model.is_active:
                cart_books_model.is_active = False
                cart_books_model.save()
            else:
                error = True
                errorMessage = "Book is already deleted from cart"
        except:
            error = True
            errorMessage = "Book not found in cart"
        cart_count = User_cart.objects.filter(is_active=True, user_id_id__exact=int(user_profile_id)).count()

    elif device_id is not None:
        try:
            cart_books_model = User_cart.objects.get(device_id__exact=int(device_id),
                                                     book_id_id__exact=int(book_id))
            books_model_to_fetch = User_cart.objects.filter(is_active=True, device_id__exact=int(device_id))
            if cart_books_model.is_active:
                cart_books_model.is_active = False
                cart_books_model.save()
            else:
                error = True
                errorMessage = "Book is already deleted from cart"
        except:
            error = True
            errorMessage = "Book not found in cart"
        cart_count = User_cart.objects.filter(is_active=True, device_id__exact=int(device_id)).count()

    total_quantity = 0
    cart_total = 0

    for book_recent in books_model_to_fetch:
        if book_recent.book_id.stock > 0:
            total_quantity += 1
            cart_total += (book_recent.book_id.price * book_recent.quantity)

    if cart_total > delivery_free_minimum_constant:
        delivery_charge = 0
    else:
        delivery_charge = delivery_charge_normal_constant
    total_amount = cart_total + delivery_charge

    return JsonResponse(
        {'error': error, 'errorMessage': errorMessage, 'cart_count': cart_count, 'total_quantity': total_quantity,
         'cart_total': cart_total, 'delivery_charge': delivery_charge, 'total_amount': total_amount})


@csrf_exempt
def view_cart_request(request):
    user_profile_id = request.POST.get('user_profile_id', None)
    device_id = request.POST.get('device_id', None)

    books_model_to_fetch = []
    if user_profile_id is not None:
        try:
            books_model_to_fetch = User_cart.objects.filter(is_active=True, user_id_id__exact=int(
                user_profile_id)).order_by('-date_added')
        except:
            pass
    elif device_id is not None:
        try:
            books_model_to_fetch = User_cart.objects.filter(is_active=True, device_id__exact=int(device_id)).order_by(
                '-date_added')
        except:
            pass

    total_quantity = 0
    cart_total = 0

    recently_viewed_books = []
    for book_recent in books_model_to_fetch:
        if book_recent.book_id.stock > 0:
            recently_viewed_books.append({'name': book_recent.book_id.name, 'price': book_recent.book_id.price,
                                          'image_url': book_recent.book_id.image_url.url,
                                          'id': book_recent.book_id.id, 'author': book_recent.book_id.author,
                                          'condition': book_recent.book_id.condition_is_old,
                                          'quantity': book_recent.quantity})
            total_quantity += 1
            cart_total += (book_recent.book_id.price * book_recent.quantity)

    if cart_total > delivery_free_minimum_constant:
        delivery_charge = 0
    else:
        delivery_charge = delivery_charge_normal_constant
    total_amount = cart_total + delivery_charge

    return JsonResponse({'books': recently_viewed_books, 'total_quantity': total_quantity, 'cart_total': cart_total,
                         'delivery_charge': delivery_charge, 'total_amount': total_amount})


@csrf_exempt
def view_wishlist_request(request):
    user_id = request.POST.get('user_id', None)
    user_profile_id = request.POST.get('user_profile_id', None)
    device_id = request.POST.get('device_id', None)

    books_model_to_fetch = []
    if user_profile_id is not None:
        try:
            books_model_to_fetch = User_wishlist.objects.filter(is_active=True, user_id_id__exact=int(
                user_profile_id)).order_by('-date_added')
        except:
            pass

    recently_viewed_books = []
    for book_recent in books_model_to_fetch:
        if book_recent.book_id.stock > 0:
            recently_viewed_books.append({'name': book_recent.book_id.name, 'price': book_recent.book_id.price,
                                          'image_url': book_recent.book_id.image_url.url,
                                          'id': book_recent.book_id.id, 'author': book_recent.book_id.author})

    return JsonResponse({'books': recently_viewed_books})


@csrf_exempt
def add_or_edit_address(request):
    user_profile_id = request.POST.get('user_profile_id', None)
    device_id = request.POST.get('device_id', None)
    name = request.POST.get('name')
    address_line_1 = request.POST.get('address_line_1')
    address_line_2 = request.POST.get('address_line_2')
    city = request.POST.get('city')
    state = request.POST.get('state')
    pincode = request.POST.get('pincode')
    mobile_number = request.POST.get('mobile_number')
    address_id = request.POST.get('address_id', None)

    error = False

    address = None
    if address_id is None:
        address = Address(name=name, address_line_1=address_line_1, address_line_2=address_line_2, city=city,
                          state=state, pincode=pincode, mobile_number=mobile_number, is_active=True,
                          device_id=device_id)
        user_profile = UserProfiles.objects.get(pk=int(user_profile_id))
        address.user_id = user_profile
        address.save()
    else:
        try:
            address = Address.objects.get(pk=int(address_id))
            address.name = name
            address.address_line_1 = address_line_1
            address.address_line_2 = address_line_2
            address.city = city
            address.state = state
            address.pincode = pincode
            address.mobile_number = mobile_number
            address.device_id = device_id
            address.save()
        except:
            error = True
    return JsonResponse({'error': error, 'id': address.id})


@csrf_exempt
def view_reviews(request):
    user_profile_id = request.POST.get('user_profile_id', None)
    device_id = request.POST.get('device_id', None)

    bookid = request.POST.get('bookid')

    reviews = []
    reviews_model = Reviews.objects.filter(is_approved=True, book_id=int(bookid)).order_by('-timestamp')
    for review in reviews_model:
        if review.is_by_registered_user:
            try:
                reviews.append(
                    {'name': review.user_id.full_name, 'image': review.user_id.profile_image, 'rating': review.rating,
                     'timestamp': review.timestamp, 'review': review.comment})
            except:
                pass
        else:
            reviews.append(
                {'name': review.name, 'rating': review.rating, 'timestamp': review.timestamp, 'review': review.comment})

    return JsonResponse({'reviews': reviews})


@csrf_exempt
def add_review(request):
    user_profile_id = request.POST.get('user_profile_id', None)
    device_id = request.POST.get('device_id', None)

    name = request.POST.get('name')
    email = request.POST.get('email')
    review = request.POST.get('review')
    bookid = request.POST.get('bookid')
    rating = request.POST.get('rating')

    error = False

    try:
        review_obj = None
        if user_profile_id is None:
            review_obj = Reviews(comment=review, rating=int(rating), is_approved=False, name=name, email=email,
                                 device_id=device_id)
        else:
            review_obj = Reviews(comment=review, rating=int(rating), is_approved=False, device_id=device_id,
                                 is_by_registered_user=True)
            review_obj.user_id = get_object_or_404(UserProfiles, pk=int(user_profile_id))
    except:
        error = True

    review_obj.book_id = get_object_or_404(Books, pk=int(bookid))
    review_obj.save()

    return JsonResponse({'error': error, })


@csrf_exempt
def autocomplete_search(request):
    word = request.POST.get('search', None)

    query = Books.objects.filter(name__icontains=word).order_by('-view_count')
    results = []
    for book in query:
        results.append({'name': book.name, 'id': book.id})

    return JsonResponse({'books': results})


@csrf_exempt
def delete_recent_viewed_book(request):
    user_id = request.POST.get('user_id', None)
    user_profile_id = request.POST.get('user_profile_id', None)
    device_id = request.POST.get('device_id', None)
    book_id = request.POST.get('book_id', None)

    error = True

    if user_profile_id is not None:
        try:
            book_model = Recently_viewed_books.objects.get(user_id_id__exact=int(user_profile_id),
                                                           book_id_id__exact=int(book_id))
            book_model.is_active = False
            book_model.save()
            error = False
        except:
            error = True
    elif device_id is not None:
        try:
            book_model = Recently_viewed_books.objects.get(device_id__exact=int(device_id),
                                                           book_id_id__exact=int(book_id))
            book_model.is_active = False
            book_model.save()
            error = False
        except:
            error = True

    return JsonResponse({'error': error})


@csrf_exempt
def recently_viewed_books(request):
    user_id = request.POST.get('user_id', None)
    user_profile_id = request.POST.get('user_profile_id', None)
    device_id = request.POST.get('device_id', None)
    pagenumber = request.POST.get("pagenumber", 1)
    pagesize = request.POST.get("pagesize", 10)

    books_model_to_fetch = []
    if user_profile_id is not None:
        try:
            books_model_to_fetch = Recently_viewed_books.objects.filter(is_active=True, user_id_id__exact=int(
                user_profile_id)).order_by('-date_added')
        except:
            pass
    elif device_id is not None:
        try:
            books_model_to_fetch = Recently_viewed_books.objects.filter(is_active=True, device_id__exact=int(
                device_id)).order_by('-date_added')
        except:
            pass

    books_paginated = Paginator(books_model_to_fetch, pagesize)
    books_model_to_fetch = books_paginated.page(pagenumber)

    recently_viewed_books = []
    for book_recent in books_model_to_fetch:
        is_favourite = False
        if user_profile_id is not None:
            try:
                query = User_wishlist.objects.get(is_active=True, user_id_id__exact=int(user_profile_id),
                                                  book_id_id__exact=book_recent.book_id.id)
                is_favourite = True
            except:
                pass
        if book_recent.book_id.stock > 0:
            recently_viewed_books.append(
                {'name': book_recent.book_id.name, 'price': book_recent.book_id.price,
                 'image_url': book_recent.book_id.image_url.url,
                 'id': book_recent.book_id.id,
                 'is_favourite': is_favourite})

    next_page = None
    if books_model_to_fetch.has_next():
        next_page = books_model_to_fetch.next_page_number()

    return JsonResponse(
        {'books': recently_viewed_books, 'next_page': next_page})


@csrf_exempt
def categories_all_category(request):
    user_id = request.POST.get('user_id', None)
    user_profile_id = request.POST.get('user_profile_id', None)
    device_id = request.POST.get('device_id', None)

    main_categories = []
    main_categories_model = Categories.objects.filter(is_root=False, is_last=False)
    for category in main_categories_model:
        sub_category = []
        sub_category_model = Categories.objects.filter(parent_id=category.id)
        for sub_cat in sub_category_model:
            sub_category.append({'name': sub_cat.name, 'id': sub_cat.id, 'image_url': sub_cat.image_url.url})
        main_categories.append({'name': category.name, 'id': category.id, 'image_url': category.image_url.url,
                                'image_url_2': category.image_url_2.url, 'sub_categories': sub_category})

    return JsonResponse({'main_categories': main_categories})


@csrf_exempt
def user_profile(request):
    user_id = request.POST.get('user_id', None)
    user_profile_id = request.POST.get('user_profile_id', None)
    device_id = request.POST.get('device_id', None)

    user_profile = get_object_or_404(UserProfiles, pk=int(user_profile_id))

    background_image_array = []
    background_images = UserProfileBackgroundImages.objects.all()
    for image in background_images:
        background_image_array.append(
            {'background_image_1': image.background_image_1.url, 'background_image_2': image.background_image_2.url})

    return JsonResponse(
        {'first_name': user_profile.first_name, 'full_name': user_profile.full_name, 'email': user_profile.email,
         'mobile_number': user_profile.mobile_number, 'profile_image': user_profile.profile_image,
         'background_images': background_image_array})


@csrf_exempt
def book_detail(request):
    user_id = request.POST.get('user_id', None)
    user_profile_id = request.POST.get('user_profile_id', None)
    device_id = request.POST.get('device_id', None)
    book_id = request.POST.get('book_id')

    book = get_object_or_404(Books, pk=int(book_id))
    book.view_count += 1
    book.save()

    if user_profile_id is not None:
        try:
            recently_viewed_books = Recently_viewed_books.objects.get(user_id_id__exact=int(user_profile_id),
                                                                      book_id_id__exact=int(book.id))
            if recently_viewed_books.is_active == True:
                recently_viewed_books.save()
                pass
            else:
                recently_viewed_books.is_active = True
                recently_viewed_books.save()
        except:
            recent_viewed_book = Recently_viewed_books(is_active=True, book_id=book)
            user_profile = UserProfiles.objects.get(pk=int(user_profile_id))
            recent_viewed_book.user_id = user_profile
            recent_viewed_book.save()
    elif device_id is not None:
        try:
            recently_viewed_books = Recently_viewed_books.objects.get(device_id__exact=device_id,
                                                                      book_id_id__exact=int(book.id))
            if recently_viewed_books.is_active == True:
                recently_viewed_books.save()
                pass
            else:
                recently_viewed_books.is_active = True
                recently_viewed_books.save()
        except:
            recent_viewed_book = Recently_viewed_books(is_active=True, book_id=book)
            recent_viewed_book.device_id = device_id
            recent_viewed_book.save()

    related_books = []
    tags = book.tags_id.all()
    for tag in tags:
        temp_books = tag.books_set.all()
        for temp_book in temp_books:
            if temp_book.id != book.id and temp_book.stock > 0:
                related_books.append(temp_book)
    related_books = set(related_books)
    related_books = list(related_books)
    related_books = related_books[:20]
    book_similar = []
    for book_temp in related_books:
        book_similar.append({'name': book_temp.name, 'price': book_temp.price, 'image_url': book_temp.image_url.url,
                             'id': book_temp.id})

    number_of_reviews = Reviews.objects.filter(book_id__exact=int(book_id), is_approved=True).order_by(
        '-timestamp').count()
    number_of_likes = User_wishlist.objects.filter(book_id__exact=int(book_id), is_active=True).count()

    is_favourite = False
    if user_profile_id is not None:
        try:
            query = User_wishlist.objects.get(is_active=True, user_id_id__exact=int(user_profile_id),
                                              book_id_id__exact=book.id)
            is_favourite = True
        except:
            is_favourite = False

    return JsonResponse(
        {"image": book.image_url.url, 'name': book.name, 'description': book.description, 'author': book.author,
         'mrp': book.mrp, 'price': book.price, 'condition': book.condition_is_old,
         "number_of_reviews": number_of_reviews, 'number_of_likes': number_of_likes, 'is_favourite': is_favourite,
         'book_id': book.id, 'related_books': book_similar, 'publisher': book.publisher, 'isbn': book.isbn,
         'binding': book.binding, 'edition': book.edition, 'language': book.language,
         'number_of_pages': book.number_of_pages, 'publication_year': book.publication_year})


@csrf_exempt
def related_books_request(request):
    user_id = request.POST.get('user_id', None)
    user_profile_id = request.POST.get('user_profile_id', None)
    device_id = request.POST.get('device_id', None)
    book_id = request.POST.get('book_id')

    book = get_object_or_404(Books, pk=int(book_id))

    related_books = []
    tags = book.tags_id.all()
    for tag in tags:
        temp_books = tag.books_set.all()
        for temp_book in temp_books:
            if temp_book.id != book.id and temp_book.stock > 0:
                related_books.append(temp_book)
    related_books = set(related_books)
    related_books = list(related_books)
    related_books = related_books[:20]
    book_similar = []
    for book in related_books:
        book_similar.append({'name': book.name, 'price': book.price, 'image_url': book.image_url.url, 'id': book.id})

    return JsonResponse({'similar_books': book_similar})


@csrf_exempt
def home_request_1(request):
    user_id = request.POST.get('user_id', None)
    user_profile_id = request.POST.get('user_profile_id', None)
    device_id = request.POST.get('device_id', None)

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
        is_favourite = False
        if user_profile_id is not None:
            try:
                query = User_wishlist.objects.get(is_active=True, user_id_id__exact=int(user_profile_id),
                                                  book_id_id__exact=book.id)
                is_favourite = True
            except:
                pass
        featured_books.append({'name': book.name, 'price': book.price, 'image_url': book.image_url.url, 'id': book.id,
                               'is_favourite': is_favourite})

    best_selling_books_model = Books.objects.filter(stock__gt=0, ).order_by('-sell_count')[:10]
    best_selling_books = []
    for book in best_selling_books_model:
        if user_profile_id is not None:
            is_favourite = False
            try:
                query = User_wishlist.objects.get(is_active=True, user_id_id__exact=int(user_profile_id),
                                                  book_id_id__exact=book.id)
                is_favourite = True
            except:
                pass
        best_selling_books.append(
            {'name': book.name, 'price': book.price, 'image_url': book.image_url.url, 'id': book.id,
             'is_favourite': is_favourite})

    wishlist_count = 0
    try:
        wishlist_count = User_wishlist.objects.filter(is_active=True, user_id_id__exact=int(
            user_profile_id)).count()
    except:
        wishlist_count = 0

    cart_count = 0
    if user_profile_id is not None:
        try:
            cart_count = User_cart.objects.filter(is_active=True, user_id_id__exact=int(
                user_profile_id)).count()
        except:
            cart_count = 0
    elif device_id is not None:
        try:
            cart_count = User_cart.objects.filter(is_active=True, device_id__exact=int(device_id)).count()
        except:
            cart_count = 0

    return JsonResponse({'banners': banners, 'categories': categories, 'featured_books': featured_books,
                         'best_selling_books': best_selling_books, 'wishlist_count': wishlist_count,
                         'cart_count': cart_count})


@csrf_exempt
def home_request_2(request):
    user_id = request.POST.get('user_id', None)
    user_profile_id = request.POST.get('user_profile_id', None)
    device_id = request.POST.get('device_id', None)

    latest_books_model = Books.objects.filter(stock__gt=0).order_by('-upload_date')[:10]
    latest_books = []
    for book in latest_books_model:
        is_favourite = False
        if user_profile_id is not None:
            try:
                query = User_wishlist.objects.get(is_active=True, user_id_id__exact=int(user_profile_id),
                                                  book_id_id__exact=book.id)
                is_favourite = True
            except:
                pass
        latest_books.append(
            {'name': book.name, 'price': book.price, 'image_url': book.image_url.url, 'id': book.id,
             'is_favourite': is_favourite})

    top_rated_books_model = Books.objects.filter(stock__gt=0).order_by('-view_count')[:10]
    top_rated_books = []
    for book in top_rated_books_model:
        is_favourite = False
        if user_profile_id is not None:
            try:
                query = User_wishlist.objects.get(is_active=True, user_id_id__exact=int(user_profile_id),
                                                  book_id_id__exact=book.id)
                is_favourite = True
            except:
                pass
        top_rated_books.append(
            {'name': book.name, 'price': book.price, 'image_url': book.image_url.url, 'id': book.id,
             'is_favourite': is_favourite})

    currently_active_books_model = Books.objects.filter(stock__gt=0).order_by('-last_active_time')[:10]
    currently_active_books = []
    for book in currently_active_books_model:
        is_favourite = False
        if user_profile_id is not None:
            try:
                query = User_wishlist.objects.get(is_active=True, user_id_id__exact=int(user_profile_id),
                                                  book_id_id__exact=book.id)
                is_favourite = True
            except:
                pass
        currently_active_books.append(
            {'name': book.name, 'price': book.price, 'image_url': book.image_url.url, 'id': book.id,
             'is_favourite': is_favourite})

    recently_viewed_books_model = []
    recently_viewed_books = []
    if user_profile_id is not None:
        try:
            recently_viewed_books_model = Recently_viewed_books.objects.filter(is_active=True, user_id_id__exact=int(
                user_profile_id)).order_by('-date_added')[:10]
        except:
            pass
    elif device_id is not None:
        try:
            recently_viewed_books_model = Recently_viewed_books.objects.filter(is_active=True, device_id__exact=int(
                device_id)).order_by('-date_added')[:10]
        except:
            pass
    for book_recent in recently_viewed_books_model:
        is_favourite = False
        if user_profile_id is not None:
            try:
                query = User_wishlist.objects.get(is_active=True, user_id_id__exact=int(user_profile_id),
                                                  book_id_id__exact=book_recent.book_id.id)
                is_favourite = True
            except:
                pass
        if book_recent.book_id.stock > 0:
            recently_viewed_books.append(
                {'name': book_recent.book_id.name, 'price': book_recent.book_id.price,
                 'image_url': book_recent.book_id.image_url.url,
                 'id': book_recent.book_id.id,
                 'is_favourite': is_favourite})

    tags_model = Tags.objects.all()[:20]
    tags = []
    for tag in tags_model:
        tags.append({'tag_name': tag.tag_name, 'id': tag.id})

    return JsonResponse({'latest_books': latest_books, 'top_rated_books': top_rated_books,
                         'currently_active_books': currently_active_books, 'tags': tags,
                         'recently_viewed_books': recently_viewed_books})


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
        device_id = request.POST.get('device_id')
        gcm_token = request.POST.get('gcm_token')

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
            user_profile.device_id = device_id
            user_profile.save()
            #  gcm work
            try:
                gcm_model = GCMDevice.objects.get(user=user)
                gcm_model.registration_id = gcm_token
                gcm_model.save()
            except:
                pass
            # end gcm work
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
            user_profile.device_id = device_id
            user_profile.userIDAuth = user_id
            user_profile.is_google_account = is_google_login
            user_profile.access_token = access_token
            user_profile.profile_details_json_object = profile_object
            user_profile.profile_image = image_url
            user_profile.login_count = 1
            user_profile.is_logged_in = True
            user_profile.save()
            # gcm work
            gcm_device_model = GCMDevice(name=name, user=user, device_id=device_id, registration_id=gcm_token)
            gcm_device_model.save()
            # end gcm work
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                status = True
                user_profile_id_to_send = user_profile.id
                user_id_to_send = user.id
        return JsonResponse({"status": status, "user_profile_id": user_profile_id_to_send, "user_id": user_id_to_send})


@csrf_exempt
def logout_view(request):
    status = False
    user_profile_id = request.POST.get('user_profile_id', None)

    try:
        logout(request)
        user_profile = UserProfiles.objects.get(pk=int(user_profile_id))
        user_profile.is_logged_in = False
        user_profile.save()
        status = True
    except:
        pass

    return JsonResponse({'status': status})


def parseBoolean(stringToParse):
    if stringToParse == 'True' or stringToParse == "true" or stringToParse == 1 or stringToParse == True or stringToParse == 'TRUE':
        return True
    return False
