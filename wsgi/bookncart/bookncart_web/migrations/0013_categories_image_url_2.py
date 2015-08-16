# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookncart_web', '0012_categories_image_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='categories',
            name='image_url_2',
            field=models.ImageField(upload_to='categories_images', blank=True, max_length=255, null=True),
        ),
    ]
