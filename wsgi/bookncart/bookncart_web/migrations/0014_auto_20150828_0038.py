# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookncart_web', '0013_categories_image_url_2'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recently_viewed_books',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('date_added', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('device_id', models.TextField(null=True, blank=True, max_length=200)),
                ('book_id', models.ForeignKey(to='bookncart_web.Books')),
                ('user_id', models.ForeignKey(null=True, to='bookncart_web.UserProfiles', blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='user_cart',
            name='device_id',
            field=models.TextField(null=True, blank=True, max_length=200),
        ),
    ]
