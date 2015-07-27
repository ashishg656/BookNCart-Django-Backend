# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookncart_web', '0005_userprofiles_is_logged_in'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofiles',
            name='token_issue_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
