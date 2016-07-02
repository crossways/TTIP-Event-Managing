# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transportation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transportationbreaks',
            name='zip_code',
            field=models.PositiveIntegerField(verbose_name='Postleitzahl'),
        ),
        migrations.AlterField(
            model_name='transportationoffer',
            name='destiny_zip_code',
            field=models.PositiveIntegerField(verbose_name='Postleitzahl Zielort'),
        ),
        migrations.AlterField(
            model_name='transportationoffer',
            name='zip_code',
            field=models.PositiveIntegerField(verbose_name='Postleitzahl'),
        ),
        migrations.AlterField(
            model_name='transportationrequest',
            name='destiny_zip_code',
            field=models.PositiveIntegerField(verbose_name='Postleitzahl Zielort'),
        ),
        migrations.AlterField(
            model_name='transportationrequest',
            name='radius',
            field=models.PositiveIntegerField(verbose_name='Umkreis'),
        ),
    ]
