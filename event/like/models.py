# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.utils import timezone

from ..models import Event

class EventLike(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='st_event_likes')
    event = models.ForeignKey(Event, related_name='event_likes')

    date = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'event')
        ordering = ['-date', '-pk']
        verbose_name = _("like")
        verbose_name_plural = _("likes")

    def get_delete_url(self):
        return reverse('event:like:delete', kwargs={'pk': str(self.pk), })
