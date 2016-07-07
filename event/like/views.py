# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse

import json
from django.http import HttpResponse

from ..models import Event
from .models import EventLike
from .forms import LikeForm


def json_response(data=None, status=200):
    # TODO: Use JsonResponse on Django 1.7
    data = data or {}
    return HttpResponse(json.dumps(data), content_type='application/json', status=status)


@login_required
def create(request, event_id):
    event = get_object_or_404(Event.objects.exclude(user=request.user), pk=event_id)

    if request.method == 'POST':
        form = LikeForm(user=request.user, event=event, data=request.POST)

        if form.is_valid():
            like = form.save()
            like.event.increase_likes_count()

            if request.is_ajax():
                return json_response({'url_delete': like.get_delete_url(), })

            return redirect(request.POST.get('next', event.get_absolute_url()))
    else:
        form = LikeForm()

    context = {
        'form': form,
        'event': event
    }

    return render(request, 'event/like/create.html', context)


@login_required
def delete(request, pk):
    like = get_object_or_404(EventLike, pk=pk, user=request.user)

    if request.method == 'POST':
        like.delete()
        like.event.decrease_likes_count()

        if request.is_ajax():
            url = reverse('event:like:create', kwargs={'event_id': like.event.pk, })
            return json_response({'url_create': url, })

        return redirect(request.POST.get('next', like.event.get_absolute_url()))

    context = {'like': like, }

    return render(request, 'event/like/delete.html', context)
