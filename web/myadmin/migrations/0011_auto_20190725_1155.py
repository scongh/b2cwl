# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2019-07-25 11:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0010_order_paytype'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='orderid',
            new_name='uid',
        ),
    ]
