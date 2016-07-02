# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transportation', '0006_auto_20160702_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transportationbreaks',
            name='price',
            field=models.FloatField(verbose_name='Preis in Euro', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='transportationoffer',
            name='departure',
            field=models.DateTimeField(verbose_name='Abfahrtstag und Zeit'),
        ),
        migrations.AlterField(
            model_name='transportationoffer',
            name='price',
            field=models.FloatField(verbose_name='Preis in Euro', null=True, blank=True),
        ),
    ]
