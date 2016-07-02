# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transportation', '0003_auto_20160702_1405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transportationoffer',
            name='car_model',
            field=models.CharField(verbose_name='Automodell', max_length=20),
        ),
        migrations.AlterField(
            model_name='transportationoffer',
            name='company',
            field=models.BooleanField(verbose_name='Angebot eines Transportunternehmens?', default=False),
        ),
    ]
