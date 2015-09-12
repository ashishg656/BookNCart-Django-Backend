# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookncart_web', '0018_address_device_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='address_line_1',
            field=models.CharField(null=True, blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='address',
            name='address_line_2',
            field=models.CharField(null=True, blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(null=True, blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='address',
            name='mobile_number',
            field=models.CharField(null=True, blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='address',
            name='name',
            field=models.CharField(null=True, blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='address',
            name='pincode',
            field=models.CharField(null=True, blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='address',
            name='state',
            field=models.CharField(null=True, blank=True, max_length=200),
        ),
    ]
