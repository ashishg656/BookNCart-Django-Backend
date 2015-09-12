# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookncart_web', '0017_auto_20150907_0048'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='device_id',
            field=models.CharField(null=True, max_length=255, blank=True),
        ),
    ]
