# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookncart_web', '0006_userprofiles_token_issue_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofiles',
            name='token_issue_date',
        ),
    ]
