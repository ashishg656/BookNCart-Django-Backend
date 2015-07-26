# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookncart_web', '0004_auto_20150726_2155'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofiles',
            name='is_logged_in',
            field=models.BooleanField(default=False),
        ),
    ]
