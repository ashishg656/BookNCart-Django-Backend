# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookncart_web', '0014_auto_20150828_0038'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofiles',
            name='device_id',
            field=models.TextField(null=True, blank=True, max_length=200),
        ),
    ]
