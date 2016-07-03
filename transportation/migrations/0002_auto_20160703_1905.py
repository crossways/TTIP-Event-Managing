# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transportation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transportationrequest',
            name='transporation_break',
            field=models.ForeignKey(blank=True, to='transportation.TransportationBreaks', null=True),
        ),
        migrations.AlterField(
            model_name='transportationrequest',
            name='transporation_offer',
            field=models.ForeignKey(blank=True, to='transportation.TransportationOffer', null=True),
        ),
    ]
