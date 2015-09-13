# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookncart_web', '0020_reviews_device_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviews',
            name='is_by_registered_user',
            field=models.BooleanField(default=False),
        ),
    ]
