# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='continuing',
            field=models.BooleanField(default=False, verbose_name='Längerwährendes Projekt'),
        ),
        migrations.AlterField(
            model_name='event',
            name='street',
            field=models.CharField(verbose_name='Straße', blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='event',
            name='zip_code',
            field=models.CharField(verbose_name='Postleitzahl', blank=True, max_length=5),
        ),
    ]
