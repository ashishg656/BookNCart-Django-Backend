from django.db import models
from django.contrib.auth.models import User


class Address(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    address_line_1 = models.CharField(max_length=200, null=True, blank=True)
    address_line_2 = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)
    mobile_number = models.CharField(max_length=20, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    user_id = models.ForeignKey('UserProfiles')
    device_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class Banners(models.Model):
    banner_image = models.ImageField(upload_to='banners', max_length=255)
    active = models.BooleanField(default=True)
    upload_date = models.DateTimeField(auto_now=True)


class Books(models.Model):
    name = models.CharField(max_length=400, db_index=True)
    description = models.TextField()
    author = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200)
    isbn = models.CharField(max_length=20)
    mrp = models.IntegerField()
    price = models.IntegerField()
    stock = models.IntegerField()
    is_featured = models.BooleanField()
    view_count = models.IntegerField()
    sell_count = models.IntegerField()
    upload_date = models.DateTimeField(auto_now=True)
    condition_is_old = models.BooleanField()
    binding = models.CharField(max_length=200)
    edition = models.CharField(max_length=200)
    language = models.CharField(max_length=200)
    number_of_pages = models.IntegerField()
    publication_year = models.DateField()
    is_active = models.BooleanField(default=True)
    image_url = models.ImageField(upload_to='books_images/%Y/%m/%d/', max_length=255)
    categories_id = models.ManyToManyField('Categories')
    tags_id = models.ManyToManyField('Tags')
    last_active_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class Books_ordered(models.Model):
    name = models.CharField(max_length=200)
    mrp = models.IntegerField()
    price = models.IntegerField()
    description = models.TextField()
    author = models.CharField(max_length=200)
    quantity = models.IntegerField()
    amount = models.IntegerField()
    condition_is_old = models.BooleanField()
    edition = models.CharField(max_length=200)
    order_id = models.ForeignKey('Orders')
    book_id = models.ForeignKey('Books')

    def __str__(self):
        return self.name


class Categories(models.Model):
    parent_id = models.ForeignKey('self', null=True, blank=True)
    name = models.CharField(max_length=200)
    image_url = models.ImageField(upload_to='categories_images', max_length=255, null=True, blank=True)
    image_url_2 = models.ImageField(upload_to='categories_images', max_length=255, null=True, blank=True)
    is_root = models.BooleanField()
    is_last = models.BooleanField()

    def __str__(self):
        return self.name


class Location(models.Model):
    latitude = models.CharField(max_length=50, null=True, blank=True)
    longitude = models.CharField(max_length=50, null=True, blank=True)
    device_id = models.CharField(max_length=200, null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    http_get_host = models.CharField(max_length=255, null=True, blank=True)
    http_host = models.CharField(max_length=255, null=True, blank=True)
    http_referer = models.CharField(max_length=255, null=True, blank=True)
    http_user_agent = models.CharField(max_length=255, null=True, blank=True)
    remote_host = models.CharField(max_length=255, null=True, blank=True)
    remote_addr = models.CharField(max_length=255, null=True, blank=True)
    remote_user = models.CharField(max_length=255, null=True, blank=True)
    user_id = models.ForeignKey('UserProfiles', null=True, blank=True)


class Orders(models.Model):
    amount = models.IntegerField()
    date_placed = models.DateTimeField(auto_now_add=True)
    paid_or_unpaid = models.BooleanField(default=False)
    number_of_items = models.IntegerField()
    expected_delivery_date = models.DateTimeField()
    shipping_fee = models.IntegerField()
    is_ready = models.BooleanField(default=False)
    ready_date = models.DateTimeField(null=True, blank=True)
    is_in_transit = models.BooleanField(default=False)
    in_transit_date = models.DateTimeField(null=True, blank=True)
    is_delivered = models.BooleanField(default=False)
    delivered_date = models.DateTimeField(null=True, blank=True)
    is_cancelled = models.BooleanField(default=False)
    cancelled_date = models.DateTimeField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)
    returned_date = models.DateTimeField(null=True, blank=True)
    location_id = models.OneToOneField(Location)
    user_id = models.ForeignKey('UserProfiles')

    def __str__(self):
        return self.amount


class Reviews(models.Model):
    comment = models.CharField(max_length=1000)
    rating = models.IntegerField()
    is_approved = models.BooleanField(default=False)
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    user_id = models.ForeignKey('UserProfiles', null=True, blank=True)
    book_id = models.ForeignKey(Books)
    timestamp = models.DateTimeField(auto_now_add=True)
    device_id = models.CharField(max_length=255, null=True, blank=True)
    is_by_registered_user = models.BooleanField(default=False)

    def __str__(self):
        return self.comment


class Tags(models.Model):
    tag_name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.tag_name


class UserProfiles(models.Model):
    full_name = models.CharField(max_length=200, null=True, blank=True)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    middle_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    password = models.CharField(max_length=150, null=True, blank=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    userIDAuth = models.CharField(max_length=200, default='')
    account_creation_date = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    mobile_number = models.CharField(max_length=20, null=True, blank=True)
    is_email_verified = models.BooleanField(default=True)
    is_google_account = models.BooleanField(default=True)
    access_token = models.TextField(null=True, blank=True)
    long_live_access_token = models.TextField(null=True, blank=True)
    google_id_token = models.TextField(null=True, blank=True)
    access_token_expires_in = models.CharField(max_length=200, null=True, blank=True)
    long_live_access_token_expires_in = models.CharField(max_length=200, null=True, blank=True)
    granted_scopes = models.TextField(null=True, blank=True)
    signed_request = models.CharField(max_length=200, null=True, blank=True)
    profile_details_json_object = models.TextField(null=True, blank=True)
    profile_image = models.TextField(null=True, blank=True)
    login_count = models.IntegerField(default=1)
    is_logged_in = models.BooleanField(default=False)
    user_link_obj = models.OneToOneField(User, null=True)
    device_id = models.TextField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.username


class UserProfileBackgroundImages(models.Model):
    background_image_1 = models.ImageField(upload_to='user profile images', max_length=255)
    background_image_2 = models.ImageField(upload_to='user profile images', max_length=255)


class User_cart(models.Model):
    quantity = models.IntegerField()
    date_added = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    user_id = models.ForeignKey(UserProfiles, null=True, blank=True)
    device_id = models.TextField(max_length=200, null=True, blank=True)
    book_id = models.ForeignKey(Books)


class User_wishlist(models.Model):
    date_added = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    user_id = models.ForeignKey(UserProfiles)
    book_id = models.ForeignKey(Books)


class Recently_viewed_books(models.Model):
    date_added = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    user_id = models.ForeignKey(UserProfiles, null=True, blank=True)
    device_id = models.TextField(max_length=200, null=True, blank=True)
    book_id = models.ForeignKey(Books)
