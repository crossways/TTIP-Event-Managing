# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EventLike',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('event', models.ForeignKey(to='event.Event', related_name='event_likes')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='st_event_likes')),
            ],
            options={
                'verbose_name': 'like',
                'ordering': ['-date', '-pk'],
                'verbose_name_plural': 'likes',
            },
        ),
        migrations.AlterUniqueTogether(
            name='eventlike',
            unique_together=set([('user', 'event')]),
        ),
    ]
