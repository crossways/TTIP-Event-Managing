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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(verbose_name='Bezeichnung', max_length=50)),
                ('location', models.CharField(verbose_name='Stadt mit Großdemo', choices=[('Berlin', 'Berlin'), ('Frankfurt', 'Frankfurt'), ('Hamburg', 'Hamburg'), ('Köln', 'Köln'), ('Leipzig', 'Leipzig'), ('München', 'München'), ('Stuttgart', 'Stuttgart')], blank=True, max_length=50)),
                ('other_location', models.CharField(verbose_name='Stadt ohne Großdemo', blank=True, max_length=50)),
                ('zip_code', models.CharField(verbose_name='Postleitzahl', max_length=5)),
                ('street', models.CharField(verbose_name='Straße', choices=[('Berlin', 'Berlin'), ('Frankfurt', 'Frankfurt'), ('Hamburg', 'Hamburg'), ('Köln', 'Köln'), ('Leipzig', 'Leipzig'), ('München', 'München'), ('Stuttgart', 'Stuttgart')], blank=True, max_length=50)),
                ('lat', models.FloatField(verbose_name='Latitude')),
                ('long', models.FloatField(verbose_name='Longitude')),
                ('date', models.DateTimeField(verbose_name='Veranstaltungstag und Zeit')),
                ('description', models.TextField(verbose_name='Beschreibung', blank=True, max_length=1000)),
                ('telephone', models.CharField(verbose_name='Festnetznummer', blank=True, max_length=20)),
                ('mobile', models.CharField(verbose_name='Mobilnummer', blank=True, max_length=20)),
                ('email', models.CharField(verbose_name='Email', blank=True, max_length=50)),
                ('likes_count', models.PositiveIntegerField(verbose_name='likes count', default=0)),
                ('cancelled', models.BooleanField(verbose_name='Event storniert', default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(unique=True)),
                ('user', models.ForeignKey(verbose_name='Benutzer', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
            },
        ),
        migrations.CreateModel(
            name='SupportNeeded',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('vacancy', models.CharField(verbose_name='Aufgabengebiet / Berufsbezeichnung', max_length=100)),
                ('description', models.TextField(verbose_name='Beschreibung', blank=True, max_length=300)),
                ('cancelled', models.BooleanField(verbose_name='Gelöscht', default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('event', models.ForeignKey(to='event.Event')),
                ('user', models.ForeignKey(verbose_name='Benutzer', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Hilfsgesuch',
                'verbose_name_plural': 'Hilfsgesuche',
            },
        ),
        migrations.CreateModel(
            name='SupportOffer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('text', models.TextField(verbose_name='Nachricht', blank=True, max_length=800)),
                ('mobile', models.CharField(verbose_name='Mobilnummer', blank=True, max_length=20)),
                ('cancelled', models.BooleanField(verbose_name='Angebot stornieren/ablehnen.', default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('event', models.ForeignKey(to='event.Event')),
                ('user', models.ForeignKey(verbose_name='Benutzer', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Hilfsangebot',
                'verbose_name_plural': 'Hilfsangebote',
            },
        ),
    ]
