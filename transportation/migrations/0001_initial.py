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
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('location', models.CharField(max_length=50, verbose_name='Ort')),
                ('street', models.CharField(max_length=70, verbose_name='Straße')),
                ('zip_code', models.PositiveIntegerField(verbose_name='Postleitzahl')),
                ('price', models.FloatField(null=True, verbose_name='Preis in Euro', blank=True)),
                ('rank', models.PositiveIntegerField(verbose_name='Haltenummer')),
                ('lat', models.FloatField(verbose_name='Latitude')),
                ('long', models.FloatField(verbose_name='Longitude')),
            ],
            options={
                'verbose_name_plural': 'Zwischenstopps',
                'verbose_name': 'Zwischenstopp',
            },
        ),
        migrations.CreateModel(
            name='TransportationOffer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('company', models.BooleanField(default=False, verbose_name='Angebot eines Transportunternehmens?')),
                ('car_manufacturer', models.CharField(max_length=20, verbose_name='Automarke')),
                ('car_model', models.CharField(max_length=20, verbose_name='Automodell')),
                ('seats_available', models.PositiveIntegerField(verbose_name='Freie Sitzplätze')),
                ('departure_location', models.CharField(max_length=50, verbose_name='Abfahrtsort')),
                ('zip_code', models.PositiveIntegerField(verbose_name='Postleitzahl Abfahrtsort')),
                ('departure_street', models.CharField(max_length=70, verbose_name='Straße Abfahrtsort')),
                ('departure', models.DateTimeField(verbose_name='Abfahrtstag und Zeit')),
                ('lat', models.FloatField(verbose_name='Latitude')),
                ('long', models.FloatField(verbose_name='Longitude')),
                ('destiny_location', models.CharField(max_length=50, verbose_name='Zielort')),
                ('destiny_zip_code', models.PositiveIntegerField(verbose_name='Postleitzahl Zielort')),
                ('destiny_street', models.CharField(max_length=70, verbose_name='Straße Zielort')),
                ('destiny_lat', models.FloatField(verbose_name='Latitude')),
                ('destiny_long', models.FloatField(verbose_name='Longitude')),
                ('mobile', models.CharField(max_length=20, verbose_name='Mobilnummer', blank=True)),
                ('price', models.FloatField(null=True, verbose_name='Preis in Euro', blank=True)),
                ('additional_breaks', models.BooleanField(default=False, verbose_name='Ungeplante Zwischenstopps möglich?')),
                ('slug', models.SlugField(unique=True)),
                ('breaks', models.ManyToManyField(to='transportation.TransportationBreaks')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Benutzer')),
            ],
            options={
                'verbose_name_plural': 'Fahrtangebote',
                'verbose_name': 'Fahrtangebot',
            },
        ),
        migrations.CreateModel(
            name='TransportationRequest',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('passengers', models.PositiveIntegerField(verbose_name='Mitfahrer insgesamt')),
                ('mobile', models.CharField(max_length=20, verbose_name='Mobilnummer', blank=True)),
                ('accepted_by_receiver', models.BooleanField(default=False, verbose_name='Anfrage akzeptieren.')),
                ('cancelled', models.BooleanField(default=False, verbose_name='Anfrage stornieren/ablehnen.')),
                ('transporation_offer', models.ForeignKey(to='transportation.TransportationOffer')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Benutzer')),
            ],
        ),
        migrations.CreateModel(
            name='TransportationSearch',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('passengers', models.PositiveIntegerField(verbose_name='Mitfahrer insgesamt')),
                ('location', models.CharField(max_length=50, verbose_name='Ort')),
                ('zip_code', models.PositiveIntegerField(verbose_name='Postleitzahl')),
                ('street', models.CharField(max_length=70, verbose_name='Straße', blank=True)),
                ('lat', models.FloatField(verbose_name='Latitude')),
                ('long', models.FloatField(verbose_name='Longitude')),
                ('radius', models.PositiveIntegerField(verbose_name='Umkreis')),
                ('departure', models.DateField(verbose_name='Reisetag')),
                ('destiny_location', models.CharField(max_length=50)),
                ('destiny_zip_code', models.PositiveIntegerField(verbose_name='Postleitzahl Zielort')),
                ('destiny_lat', models.FloatField(verbose_name='Latitude')),
                ('destiny_long', models.FloatField(verbose_name='Longitude')),
                ('mobile', models.CharField(max_length=20, verbose_name='Mobilnummer', blank=True)),
                ('slug', models.SlugField(unique=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Benutzer')),
            ],
            options={
                'verbose_name_plural': 'Fahrtanfragen',
                'verbose_name': 'Fahrtanfrage',
            },
        ),
    ]
