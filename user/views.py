from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponsePermanentRedirect

from djconfig import config

from spirit.core.utils.paginator import yt_paginate
from transportation.models import TransportationOffer, TransportationRequest

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
    user_recipes = TransportationOffer.objects\
        .filter(user_id=pk)\
        .order_by('-timestamp')

    return _activity(
        request, pk, slug,
        queryset=user_recipes,
        template='resistance/user/transportation_profil.html',
        reverse_to='resistance:user:view_your_recipes',
        context_name='recipes',
        per_page=config.comments_per_page,
    )

def test(request, pk, slug):
    pass