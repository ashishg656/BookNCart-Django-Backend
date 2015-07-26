# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookncart_web', '0003_auto_20150726_2141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofiles',
            name='login_count',
            field=models.IntegerField(default=1),
        ),
    ]
