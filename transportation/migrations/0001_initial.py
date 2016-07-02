# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TransportationBreaks',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('location', models.CharField(max_length=50, verbose_name='Ort')),
                ('zip_code', models.PositiveIntegerField(max_length=5, verbose_name='Postleitzahl')),
                ('lat', models.FloatField(verbose_name='Latitude')),
                ('long', models.FloatField(verbose_name='Longitude')),
                ('rank', models.PositiveIntegerField(max_length=2, verbose_name='Haltenummer')),
            ],
        ),
        migrations.CreateModel(
            name='TransportationOffer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('company', models.BooleanField(default=False)),
                ('car_manufacturer', models.CharField(max_length=20, verbose_name='Automarke')),
                ('car_model', models.CharField(max_length=20)),
                ('seats_available', models.PositiveIntegerField(verbose_name='Freie Sitzplätze')),
                ('departure_location', models.CharField(max_length=50, verbose_name='Ort')),
                ('zip_code', models.PositiveIntegerField(max_length=5, verbose_name='Postleitzahl')),
                ('departure_street', models.CharField(max_length=70, blank=True, verbose_name='Straße')),
                ('departure', models.DateTimeField(verbose_name='Abfahrtszeit')),
                ('lat', models.FloatField(verbose_name='Latitude')),
                ('long', models.FloatField(verbose_name='Longitude')),
                ('destiny_location', models.CharField(max_length=50)),
                ('destiny_zip_code', models.PositiveIntegerField(max_length=5, verbose_name='Postleitzahl Zielort')),
                ('destiny_lat', models.FloatField(verbose_name='Latitude')),
                ('destiny_long', models.FloatField(verbose_name='Longitude')),
                ('mobile', models.CharField(max_length=20, blank=True, verbose_name='Mobilnummer')),
                ('additional_breaks', models.BooleanField(default=False)),
                ('breaks', models.ManyToManyField(to='transportation.TransportationBreaks')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Benutzer')),
            ],
        ),
        migrations.CreateModel(
            name='TransportationRequest',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('passengers', models.PositiveIntegerField(verbose_name='Mitfahrer insgesamt')),
                ('location', models.CharField(max_length=50, verbose_name='Ort')),
                ('zip_code', models.PositiveIntegerField(max_length=5, verbose_name='Postleitzahl')),
                ('street', models.CharField(max_length=70, blank=True, verbose_name='Straße')),
                ('lat', models.FloatField(verbose_name='Latitude')),
                ('long', models.FloatField(verbose_name='Longitude')),
                ('radius', models.PositiveIntegerField(max_length=3, verbose_name='Umkreis')),
                ('departure', models.DateField(verbose_name='Reisetag')),
                ('destiny_location', models.CharField(max_length=50)),
                ('destiny_zip_code', models.PositiveIntegerField(max_length=5, verbose_name='Postleitzahl Zielort')),
                ('destiny_lat', models.FloatField(verbose_name='Latitude')),
                ('destiny_long', models.FloatField(verbose_name='Longitude')),
                ('mobile', models.CharField(max_length=20, blank=True, verbose_name='Mobilnummer')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Benutzer')),
            ],
        ),
    ]
