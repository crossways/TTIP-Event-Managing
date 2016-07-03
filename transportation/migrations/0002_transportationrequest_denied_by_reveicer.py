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
            name='denied_by_reveicer',
            field=models.BooleanField(verbose_name='Anfrage ablehnen.', default=False),
        ),
    ]
