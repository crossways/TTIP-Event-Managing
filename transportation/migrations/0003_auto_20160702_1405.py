# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transportation', '0002_auto_20160702_1405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transportationbreaks',
            name='rank',
            field=models.PositiveIntegerField(verbose_name='Haltenummer'),
        ),
        migrations.AlterField(
            model_name='transportationrequest',
            name='zip_code',
            field=models.PositiveIntegerField(verbose_name='Postleitzahl'),
        ),
    ]
