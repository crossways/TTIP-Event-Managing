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
            name='Event',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=50, verbose_name='Bezeichnung')),
                ('location', models.CharField(max_length=50, choices=[('Berlin', 'Berlin'), ('Frankfurt', 'Frankfurt'), ('Hamburg', 'Hamburg'), ('Köln', 'Köln'), ('Leipzig', 'Leipzig'), ('München', 'München'), ('Stuttgart', 'Stuttgart')], blank=True, verbose_name='Stadt mit Großdemo')),
                ('other_location', models.CharField(max_length=50, blank=True, verbose_name='Stadt ohne Großdemo')),
                ('zip_code', models.CharField(max_length=5, blank=True, verbose_name='Postleitzahl')),
                ('street', models.CharField(max_length=50, blank=True, verbose_name='Straße')),
                ('lat', models.FloatField(verbose_name='Latitude')),
                ('long', models.FloatField(verbose_name='Longitude')),
                ('date', models.DateTimeField(verbose_name='Veranstaltungstag und Zeit')),
                ('continuing', models.BooleanField(default=False, verbose_name='Längerwährendes Projekt')),
                ('description', models.TextField(max_length=1000, blank=True, verbose_name='Beschreibung')),
                ('telephone', models.CharField(max_length=20, blank=True, verbose_name='Festnetznummer')),
                ('mobile', models.CharField(max_length=20, blank=True, verbose_name='Mobilnummer')),
                ('email', models.CharField(max_length=50, blank=True, verbose_name='Email')),
                ('likes_count', models.PositiveIntegerField(default=0, verbose_name='likes count')),
                ('cancelled', models.BooleanField(default=False, verbose_name='Event storniert')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(unique=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Benutzer')),
            ],
            options={
                'verbose_name_plural': 'Events',
                'verbose_name': 'Event',
            },
        ),
        migrations.CreateModel(
            name='SupportNeeded',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=30, verbose_name='Aufgabengebiet / Berufsbezeichnung')),
                ('short_text', models.CharField(max_length=100, verbose_name='Kurzbeschreibung')),
                ('description', models.TextField(max_length=1000, blank=True, verbose_name='Beschreibung')),
                ('cancelled', models.BooleanField(default=False, verbose_name='Gelöscht')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(unique=True)),
                ('event', models.ForeignKey(to='event.Event')),
            ],
            options={
                'verbose_name_plural': 'Hilfsgesuche',
                'verbose_name': 'Hilfsgesuch',
            },
        ),
        migrations.CreateModel(
            name='SupportOffer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('text', models.TextField(max_length=800, blank=True, verbose_name='Nachricht')),
                ('mobile', models.CharField(max_length=20, blank=True, verbose_name='Mobilnummer')),
                ('cancelled', models.BooleanField(default=False, verbose_name='Angebot stornieren/ablehnen.')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('supportneeded', models.ForeignKey(to='event.SupportNeeded')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Benutzer')),
            ],
            options={
                'verbose_name_plural': 'Hilfsangebote',
                'verbose_name': 'Hilfsangebot',
            },
        ),
    ]
