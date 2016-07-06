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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('location', models.CharField(verbose_name='Ort', max_length=50)),
                ('street', models.CharField(verbose_name='Straße', max_length=70)),
                ('zip_code', models.CharField(verbose_name='Postleitzahl', max_length=5)),
                ('price', models.FloatField(null=True, blank=True, verbose_name='Preis in Euro')),
                ('rank', models.PositiveIntegerField(verbose_name='Haltenummer')),
                ('lat', models.FloatField(verbose_name='Latitude')),
                ('long', models.FloatField(verbose_name='Longitude')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Zwischenstopps',
                'verbose_name': 'Zwischenstopp',
            },
        ),
        migrations.CreateModel(
            name='TransportationOffer',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('company', models.BooleanField(verbose_name='Angebot eines Transportunternehmens?', default=False)),
                ('car_manufacturer', models.CharField(verbose_name='Automarke', max_length=20)),
                ('car_model', models.CharField(verbose_name='Automodell', max_length=20)),
                ('seats_available', models.PositiveIntegerField(verbose_name='Freie Sitzplätze')),
                ('departure_location', models.CharField(verbose_name='Abfahrtsort', max_length=50)),
                ('zip_code', models.CharField(verbose_name='Postleitzahl Abfahrtsort', max_length=5)),
                ('departure_street', models.CharField(verbose_name='Straße Abfahrtsort', max_length=70)),
                ('departure', models.DateTimeField(verbose_name='Abfahrtstag und Zeit')),
                ('lat', models.FloatField(verbose_name='Latitude')),
                ('long', models.FloatField(verbose_name='Longitude')),
                ('destiny_location', models.CharField(verbose_name='Zielort', max_length=50)),
                ('destiny_zip_code', models.CharField(verbose_name='Postleitzahl Zielort', max_length=5)),
                ('destiny_street', models.CharField(verbose_name='Straße Zielort', max_length=70)),
                ('destiny_lat', models.FloatField(verbose_name='Latitude')),
                ('destiny_long', models.FloatField(verbose_name='Longitude')),
                ('mobile', models.CharField(blank=True, verbose_name='Mobilnummer', max_length=20)),
                ('price', models.FloatField(null=True, blank=True, verbose_name='Preis in Euro')),
                ('cancelled', models.BooleanField(verbose_name='Fahrt storniert', default=False)),
                ('additional_breaks', models.BooleanField(verbose_name='Ungeplante Zwischenstopps möglich?', default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('passengers', models.PositiveIntegerField(verbose_name='Mitfahrer insgesamt')),
                ('text', models.TextField(blank=True, verbose_name='Nachricht', max_length=800)),
                ('mobile', models.CharField(blank=True, verbose_name='Mobilnummer', max_length=20)),
                ('accepted_by_receiver', models.BooleanField(verbose_name='Anfrage akzeptieren.', default=False)),
                ('denied_by_reveicer', models.BooleanField(verbose_name='Anfrage ablehnen.', default=False)),
                ('cancelled', models.BooleanField(verbose_name='Anfrage stornieren/ablehnen.', default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('transporation_break', models.ForeignKey(blank=True, null=True, to='transportation.TransportationBreaks')),
                ('transporation_offer', models.ForeignKey(blank=True, null=True, to='transportation.TransportationOffer')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Benutzer')),
            ],
            options={
                'verbose_name_plural': 'Fahrtanfragen',
                'verbose_name': 'Fahrtanfrage',
            },
        ),
        migrations.CreateModel(
            name='TransportationSearch',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('passengers', models.PositiveIntegerField(verbose_name='Mitfahrer insgesamt')),
                ('location', models.CharField(verbose_name='Ort', max_length=50)),
                ('zip_code', models.CharField(verbose_name='Postleitzahl', max_length=5)),
                ('street', models.CharField(blank=True, verbose_name='Straße', max_length=70)),
                ('lat', models.FloatField(verbose_name='Latitude')),
                ('long', models.FloatField(verbose_name='Longitude')),
                ('radius', models.PositiveIntegerField(verbose_name='Umkreis')),
                ('departure', models.DateField(verbose_name='Reisetag')),
                ('destiny_location', models.CharField(max_length=50)),
                ('destiny_zip_code', models.PositiveIntegerField(verbose_name='Postleitzahl Zielort')),
                ('destiny_lat', models.FloatField(verbose_name='Latitude')),
                ('destiny_long', models.FloatField(verbose_name='Longitude')),
                ('mobile', models.CharField(blank=True, verbose_name='Mobilnummer', max_length=20)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(unique=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Benutzer')),
            ],
            options={
                'verbose_name_plural': 'Fahrtsuchen',
                'verbose_name': 'Fahrtsuche',
            },
        ),
    ]
