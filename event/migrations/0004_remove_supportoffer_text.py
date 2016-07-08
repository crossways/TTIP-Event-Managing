# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0003_auto_20160708_1842'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='supportoffer',
            name='text',
        ),
    ]
