from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import render, redirect,get_object_or_404

from .forms import TransportationOfferForm, TransportationBreaksForm
from .models import TransportationOffer, TransportationBreaks, TransportationSearch

# Create your views here.

def transportation_startingpage(request):
    return render(request, 'transportation/starting_page.html')


def details(request, pk, slug):
    transportation = get_object_or_404(TransportationOffer, id=pk)
    if transportation.slug != slug:
        return HttpResponsePermanentRedirect(transportation.get_absolute_url())

    current_user = request.user

    context = {
        'current_user': current_user,
        'transportation': transportation,
    }
    return render(request, 'transportation/view_transportation.html', context, )


def search_details(request, pk, slug):
    search = get_object_or_404(TransportationSearch, id=pk)
    if search.slug != slug:
        return HttpResponsePermanentRedirect(search.get_absolute_url())

    current_user = request.user

    context = {
        'current_user': current_user,
        'transportation': search,
    }
    return render(request, 'transportation/view_search.html', context, )


@login_required
def register_transportation_offer(request):
    form = TransportationOfferForm(request.POST or None)

    if form.is_valid():
        form.cleaned_data['user'] = request.user
        transportation = TransportationOffer.objects.create(**form.cleaned_data)
        return redirect(reverse('transportation:add_additional_stops', kwargs={'pk': transportation.pk, 'slug': transportation.slug}))

    context = {
        'form': form,
    }

    return render(request, 'transportation/register_transportation_offer.html', context)


@login_required
def add_additional_stops(request, pk, slug):
    transportation = get_object_or_404(TransportationOffer, id=pk)
    if request.user != transportation.user:
        return redirect(
            reverse('transportation:details', kwargs={'pk': transportation.pk, 'slug': transportation.slug}))

    form = TransportationBreaksForm(request.POST or None)
    if form.is_valid():
        new_break = TransportationBreaks.objects.create(**form.cleaned_data)
        transportation.breaks.add(new_break)
        return redirect(
            reverse('transportation:details', kwargs={'pk': transportation.pk, 'slug': transportation.slug}))

    context = {
        'form': form,
        'transportation': transportation,
    }
    return render(request, 'transportation/add_additional_stops.html', context)