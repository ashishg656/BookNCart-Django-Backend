# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookncart_web', '0015_userprofiles_device_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfileBackgroundImages',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('background_image_1', models.ImageField(upload_to='user profile images', max_length=255)),
                ('background_image_2', models.ImageField(upload_to='user profile images', max_length=255)),
            ],
        ),
    ]
