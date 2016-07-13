# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0004_remove_supportoffer_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='supportneeded',
            name='seen',
            field=models.BooleanField(default=False, verbose_name='gesehen'),
        ),
    ]
