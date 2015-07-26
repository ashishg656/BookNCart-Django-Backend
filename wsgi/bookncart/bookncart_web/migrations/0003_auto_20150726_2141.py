# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bookncart_web', '0002_auto_20150726_2105'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofiles',
            name='name',
        ),
        migrations.AddField(
            model_name='userprofiles',
            name='access_token',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='userprofiles',
            name='access_token_expires_in',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='userprofiles',
            name='first_name',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='userprofiles',
            name='full_name',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='userprofiles',
            name='granted_scopes',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='userprofiles',
            name='is_google_account',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='userprofiles',
            name='last_name',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='userprofiles',
            name='login_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofiles',
            name='long_live_access_token',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='userprofiles',
            name='long_live_access_token_expires_in',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='userprofiles',
            name='middle_name',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='userprofiles',
            name='profile_details_json_object',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='userprofiles',
            name='profile_image',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='userprofiles',
            name='signed_request',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='userprofiles',
            name='userIDAuth',
            field=models.CharField(max_length=200, default=''),
        ),
        migrations.AddField(
            model_name='userprofiles',
            name='user_link_obj',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='userprofiles',
            name='username',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='userprofiles',
            name='email',
            field=models.EmailField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='userprofiles',
            name='is_email_verified',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='userprofiles',
            name='last_login',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='userprofiles',
            name='mobile_number',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='userprofiles',
            name='password',
            field=models.CharField(max_length=150, null=True, blank=True),
        ),
    ]
