# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import template

from .forms import LikeForm


register = template.Library()


@register.inclusion_tag('event/like/_form.html')
def render_like_form(comment, like, next=None):
    form = LikeForm()
    return {'form': form, 'comment_id': comment.pk, 'like': like, 'next': next}
