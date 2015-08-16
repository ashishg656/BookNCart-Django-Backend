# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookncart_web', '0011_auto_20150816_1407'),
    ]

    operations = [
        migrations.AddField(
            model_name='categories',
            name='image_url',
            field=models.ImageField(blank=True, null=True, upload_to='categories_images', max_length=255),
        ),
    ]
