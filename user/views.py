from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponsePermanentRedirect

from djconfig import config

from spirit.core.utils.paginator import yt_paginate
from event.models import Event, SupportNeeded, SupportOffer
from transportation.models import TransportationOffer, TransportationRequest
from event.models import Event

User = get_user_model()


@login_required
def _activity(request, pk, slug, queryset, template, reverse_to, context_name, per_page):
    p_user = get_object_or_404(User, pk=pk)

    if p_user.st.slug != slug:
        url = reverse(reverse_to, kwargs={'pk': p_user.pk, 'slug': p_user.st.slug})
        return HttpResponsePermanentRedirect(url)

    items = yt_paginate(
        queryset,
        per_page=per_page,
        page_number=request.GET.get('page', 1)
    )

    context = {
        'p_user': p_user,
        context_name: items
    }

    return render(request, template, context)

def view_transportation_in_profile(request, pk, slug):
    user = get_object_or_404(User, pk=pk)
    transportation_offers = TransportationOffer.objects\
        .filter(user=user)\
        .order_by('-timestamp')

    return _activity(
        request, pk, slug,
        queryset=transportation_offers,
        template='resistance/user/transportation_profil.html',
        reverse_to='user:view_transportation_in_profile',
        context_name='transportation_offers',
        per_page=config.comments_per_page,
    )


def view_transportation_requests_in_profile(request, pk, slug):
    user = get_object_or_404(User, pk=pk)
    transportation_requests = TransportationRequest.objects\
        .filter(user=user)\
        .order_by('-timestamp')

    return _activity(
        request, pk, slug,
        queryset=transportation_requests,
        template='resistance/user/transportation_requests_profil.html',
        reverse_to='user:view_transportation_requests_in_profile',
        context_name='transportation_requests',
        per_page=config.comments_per_page,
    )


def view_event_in_profile(request, pk, slug):
    user = get_object_or_404(User, pk=pk)
    events = Event.objects\
        .filter(user=user)\
        .order_by('-timestamp')

    return _activity(
        request, pk, slug,
        queryset=events,
        template='resistance/user/event_details_profil.html',
        reverse_to='user:view_event_in_profile',
        context_name='events',
        per_page=config.comments_per_page,
    )
