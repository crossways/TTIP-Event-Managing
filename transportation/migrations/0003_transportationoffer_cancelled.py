# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transportation', '0002_auto_20160703_0208'),
    ]

    operations = [
        migrations.AddField(
            model_name='transportationoffer',
            name='cancelled',
            field=models.BooleanField(default=False, verbose_name='Fahrt storniert'),
        ),
    ]
