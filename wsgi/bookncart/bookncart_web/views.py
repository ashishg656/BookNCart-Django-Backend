from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render
from PIL import Image
from django.template import RequestContext
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.core import serializers
import json

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
        return JsonResponse({'cart_items': cart_items, 'subtotal': subtotal, 'quantity': quantity, 'total': total,
                             'error_message': error_message})


def view_for_requestcontext_data_common_view(request):
    top_category = Categories.objects.filter(is_root__exact=1)
    sub_category = Categories.objects.filter(is_root__exact=0).filter(is_last__exact=0)
    subsub_category = Categories.objects.filter(is_last__exact=1)
    context = {'top_category': top_category,
               'sub_category': sub_category,
               'subsub_category': subsub_category}
    return context
