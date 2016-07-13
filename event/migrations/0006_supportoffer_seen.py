# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0005_supportneeded_seen'),
    ]

    operations = [
        migrations.AddField(
            model_name='supportoffer',
            name='seen',
            field=models.BooleanField(default=False, verbose_name='gesehen'),
        ),
    ]
