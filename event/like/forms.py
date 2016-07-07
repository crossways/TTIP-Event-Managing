# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import EventLike


class LikeForm(forms.ModelForm):

    class Meta:
        model = EventLike
        fields = []

    def __init__(self, user=None, event=None, *args, **kwargs):
        super(LikeForm, self).__init__(*args, **kwargs)
        self.user = user
        self.event = event

    def clean(self):
        cleaned_data = super(LikeForm, self).clean()

        like = EventLike.objects.filter(user=self.user,
                                        event=self.event)

        if like.exists():
            # Do this since some of the unique_together fields are excluded.
            raise forms.ValidationError(_("This like already exists"))

        return cleaned_data

    def save(self, commit=True):
        if not self.instance.pk:
            self.instance.user = self.user
            self.instance.event = self.event

        return super(LikeForm, self).save(commit)
