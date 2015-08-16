# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookncart_web', '0010_auto_20150728_1428'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banners',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('banner_image', models.ImageField(upload_to='banners', max_length=255)),
                ('active', models.BooleanField(default=True)),
                ('upload_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='books',
            name='last_active_time',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
