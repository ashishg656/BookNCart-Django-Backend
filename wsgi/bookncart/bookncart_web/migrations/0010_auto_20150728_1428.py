# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookncart_web', '0009_userprofiles_google_id_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofiles',
            name='granted_scopes',
            field=models.TextField(null=True, blank=True),
        ),
    ]
