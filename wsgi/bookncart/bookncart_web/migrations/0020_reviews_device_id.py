# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookncart_web', '0019_auto_20150912_1259'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviews',
            name='device_id',
            field=models.CharField(null=True, blank=True, max_length=255),
        ),
    ]
