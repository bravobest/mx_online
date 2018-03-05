# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-11-07 16:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='courseorg',
            name='catgory',
        ),
        migrations.AddField(
            model_name='courseorg',
            name='category',
            field=models.CharField(choices=[('pxjg', '\u57f9\u8bad\u673a\u6784'), ('gr', '\u4e2a\u4eba'), ('gx', '\u9ad8\u6821')], default='pxjg', max_length=24, verbose_name='\u673a\u6784\u7c7b\u522b'),
        ),
    ]