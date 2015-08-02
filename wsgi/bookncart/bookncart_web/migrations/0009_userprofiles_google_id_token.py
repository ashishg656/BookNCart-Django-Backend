# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookncart_web', '0008_auto_20150727_1606'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofiles',
            name='google_id_token',
            field=models.TextField(null=True, blank=True),
        ),
    ]
