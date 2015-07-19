# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('address_line_1', models.CharField(max_length=200)),
                ('address_line_2', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=200)),
                ('state', models.CharField(max_length=200)),
                ('pincode', models.CharField(max_length=10)),
                ('mobile_number', models.CharField(max_length=20)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Books',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=400)),
                ('description', models.TextField()),
                ('author', models.CharField(max_length=200)),
                ('publisher', models.CharField(max_length=200)),
                ('isbn', models.CharField(max_length=20)),
                ('mrp', models.IntegerField()),
                ('price', models.IntegerField()),
                ('stock', models.IntegerField()),
                ('is_featured', models.BooleanField()),
                ('view_count', models.IntegerField()),
                ('sell_count', models.IntegerField()),
                ('upload_date', models.DateTimeField(auto_now=True)),
                ('condition_is_old', models.BooleanField()),
                ('binding', models.CharField(max_length=200)),
                ('edition', models.CharField(max_length=200)),
                ('language', models.CharField(max_length=200)),
                ('number_of_pages', models.IntegerField()),
                ('publication_year', models.DateField()),
                ('is_active', models.BooleanField(default=True)),
                ('image_url', models.ImageField(max_length=255, upload_to='books_images/%Y/%m/%d/')),
            ],
        ),
        migrations.CreateModel(
            name='Books_ordered',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('mrp', models.IntegerField()),
                ('price', models.IntegerField()),
                ('description', models.TextField()),
                ('author', models.CharField(max_length=200)),
                ('quantity', models.IntegerField()),
                ('amount', models.IntegerField()),
                ('condition_is_old', models.BooleanField()),
                ('edition', models.CharField(max_length=200)),
                ('book_id', models.ForeignKey(to='bookncart_web.Books')),
            ],
        ),
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('is_root', models.BooleanField()),
                ('is_last', models.BooleanField()),
                ('parent_id', models.ForeignKey(null=True, blank=True, to='bookncart_web.Categories')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('latitude', models.CharField(max_length=50)),
                ('longitude', models.CharField(max_length=50)),
                ('device_id', models.CharField(max_length=200)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('amount', models.IntegerField()),
                ('date_placed', models.DateTimeField(auto_now_add=True)),
                ('paid_or_unpaid', models.BooleanField(default=False)),
                ('number_of_items', models.IntegerField()),
                ('expected_delivery_date', models.DateTimeField()),
                ('shipping_fee', models.IntegerField()),
                ('is_ready', models.BooleanField(default=False)),
                ('ready_date', models.DateTimeField(null=True, blank=True)),
                ('is_in_transit', models.BooleanField(default=False)),
                ('in_transit_date', models.DateTimeField(null=True, blank=True)),
                ('is_delivered', models.BooleanField(default=False)),
                ('delivered_date', models.DateTimeField(null=True, blank=True)),
                ('is_cancelled', models.BooleanField(default=False)),
                ('cancelled_date', models.DateTimeField(null=True, blank=True)),
                ('is_returned', models.BooleanField(default=False)),
                ('returned_date', models.DateTimeField(null=True, blank=True)),
                ('location_id', models.OneToOneField(to='bookncart_web.Location')),
            ],
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('comment', models.CharField(max_length=1000)),
                ('rating', models.IntegerField()),
                ('is_approved', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=200, blank=True, null=True)),
                ('email', models.EmailField(max_length=200, blank=True, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('book_id', models.ForeignKey(to='bookncart_web.Books')),
            ],
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('tag_name', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='User_cart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('quantity', models.IntegerField()),
                ('date_added', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('book_id', models.ForeignKey(to='bookncart_web.Books')),
            ],
        ),
        migrations.CreateModel(
            name='User_wishlist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('date_added', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('book_id', models.ForeignKey(to='bookncart_web.Books')),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('password', models.TextField()),
                ('account_creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_login', models.DateTimeField()),
                ('mobile_number', models.CharField(max_length=20)),
                ('is_email_verified', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='user_wishlist',
            name='user_id',
            field=models.ForeignKey(to='bookncart_web.Users'),
        ),
        migrations.AddField(
            model_name='user_cart',
            name='user_id',
            field=models.ForeignKey(null=True, blank=True, to='bookncart_web.Users'),
        ),
        migrations.AddField(
            model_name='reviews',
            name='user_id',
            field=models.ForeignKey(null=True, blank=True, to='bookncart_web.Users'),
        ),
        migrations.AddField(
            model_name='orders',
            name='user_id',
            field=models.ForeignKey(to='bookncart_web.Users'),
        ),
        migrations.AddField(
            model_name='location',
            name='user_id',
            field=models.ForeignKey(null=True, blank=True, to='bookncart_web.Users'),
        ),
        migrations.AddField(
            model_name='books_ordered',
            name='order_id',
            field=models.ForeignKey(to='bookncart_web.Orders'),
        ),
        migrations.AddField(
            model_name='books',
            name='categories_id',
            field=models.ManyToManyField(to='bookncart_web.Categories'),
        ),
        migrations.AddField(
            model_name='books',
            name='tags_id',
            field=models.ManyToManyField(to='bookncart_web.Tags'),
        ),
        migrations.AddField(
            model_name='address',
            name='user_id',
            field=models.ForeignKey(to='bookncart_web.Users'),
        ),
    ]
