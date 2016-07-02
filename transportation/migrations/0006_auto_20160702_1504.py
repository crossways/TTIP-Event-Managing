# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transportation', '0005_auto_20160702_1450'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transportationbreaks',
            options={'verbose_name': 'Zwischenstopp', 'verbose_name_plural': 'Zwischenstopps'},
        ),
        migrations.AlterModelOptions(
            name='transportationoffer',
            options={'verbose_name': 'Fahrtangebot', 'verbose_name_plural': 'Fahrtangebote'},
        ),
        migrations.AlterModelOptions(
            name='transportationrequest',
            options={'verbose_name': 'Fahrtanfrage', 'verbose_name_plural': 'Fahrtanfragen'},
        ),
        migrations.AddField(
            model_name='transportationbreaks',
            name='price',
            field=models.FloatField(verbose_name='Preis in Euro', null=True),
        ),
        migrations.AddField(
            model_name='transportationoffer',
            name='price',
            field=models.FloatField(verbose_name='Preis in Euro', null=True),
        ),
        migrations.AlterField(
            model_name='transportationbreaks',
            name='street',
            field=models.CharField(verbose_name='Straße', max_length=70),
        ),
        migrations.AlterField(
            model_name='transportationoffer',
            name='additional_breaks',
            field=models.BooleanField(verbose_name='Ungeplante Zwischenstopps möglich?', default=False),
        ),
        migrations.AlterField(
            model_name='transportationoffer',
            name='departure_location',
            field=models.CharField(verbose_name='Abfahrtsort', max_length=50),
        ),
        migrations.AlterField(
            model_name='transportationoffer',
            name='departure_street',
            field=models.CharField(verbose_name='Straße Abfahrtsort', max_length=70),
        ),
        migrations.AlterField(
            model_name='transportationoffer',
            name='destiny_location',
            field=models.CharField(verbose_name='Zielort', max_length=50),
        ),
        migrations.AlterField(
            model_name='transportationoffer',
            name='destiny_street',
            field=models.CharField(verbose_name='Straße Zielort', max_length=70),
        ),
        migrations.AlterField(
            model_name='transportationoffer',
            name='zip_code',
            field=models.PositiveIntegerField(verbose_name='Postleitzahl Abfahrtsort'),
        ),
    ]
