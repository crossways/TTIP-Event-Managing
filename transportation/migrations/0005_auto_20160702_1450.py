# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transportation', '0004_auto_20160702_1443'),
    ]

    operations = [
        migrations.AddField(
            model_name='transportationbreaks',
            name='street',
            field=models.CharField(max_length=70, verbose_name='Straße', blank=True),
        ),
        migrations.AddField(
            model_name='transportationoffer',
            name='destiny_street',
            field=models.CharField(max_length=70, verbose_name='Straße', blank=True),
        ),
    ]
