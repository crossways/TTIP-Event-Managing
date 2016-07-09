from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import UpdateView

from .models import Event, SupportNeeded, SupportOffer
from .forms import EventForm, EventSearchForm, SupportNeededForm, SupportOfferForm

from transportation.utils.geo import GeoLocation, geo_test

from datetime import datetime
# Create your views here.

class EventUpdate(UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'event/change_event.html'

    def form_valid(self, form):
        event = self.object
        Event.objects.filter(pk=event.pk).update(**form.cleaned_data)
        return redirect(
            reverse('event:event_details', kwargs={'pk': event.pk, 'slug': event.slug}))


class SupportNeededUpdate(UpdateView):
    model = SupportNeeded
    form_class = SupportNeededForm
    template_name = 'event/change_supportneeded.html'


def event_startingpage(request):
    return render(request, 'event/starting_page.html')


@login_required
def register_event(request):
    form = EventForm(request.POST or None)

    if form.is_valid():
        user = request.user
        form.cleaned_data['user'] = user

        event = Event.objects.create(**form.cleaned_data)

        return redirect(reverse('event:event_details', kwargs={'pk': event.pk, 'slug': event.slug}))

    context = {
        'form': form,
    }

    return render(request, 'event/register_event.html', context)


def event_details(request, pk, slug):
    event = get_object_or_404(Event, id=pk)
    if event.slug != slug:
        return HttpResponsePermanentRedirect(event.get_absolute_url())

    current_user = request.user
    if current_user == event.user:
        supportneeded = SupportNeeded.objects.filter(event=event)
    else:
        supportneeded = SupportNeeded.objects.filter(event=event, cancelled=False)

    supportoffers = SupportOffer.objects.filter(supportneeded__event__pk=pk)
    address = "{} {}".format(event.lat, event.long)

    context = {
        'current_user': current_user,
        'event': event,
        'supportneeded': supportneeded,
        'supportoffers': supportoffers,
        'address': address,
    }
    if current_user in [offer.user for offer in supportoffers]:
        current_user_offers = supportoffers.filter(user=current_user)
        context.update({'current_user_offers': current_user_offers})

    return render(request, 'event/event_details.html', context)


@login_required
def cancel_event_or_activate_again(request, pk, slug):
    event = Event.objects.get(id=pk)

    if request.user == event.user:
        if event.cancelled:
            event.cancelled = False
        else:
            event.cancelled = True
        event.save()

    #Todo: redirect to calling page
    return redirect(reverse('event:event_details', kwargs={'pk': event.pk, 'slug': event.slug}))


@login_required
def register_supportneeded(request, pk, slug):
    ''' Creates an SupportNeeded instance for an existing Event object '''
    form = SupportNeededForm(request.POST or None)
    if form.is_valid():
        user = request.user
        event = Event.objects.get(pk=pk)
        if user == event.user:
            form.cleaned_data['event'] = event

            supportneeded = SupportNeeded.objects.create(**form.cleaned_data)

            return redirect(reverse('event:supportneeded_details',
                                    kwargs={'pk': event.pk,
                                            'slug': event.slug,
                                            'support_pk': supportneeded.pk,
                                            'support_slug': supportneeded.slug,
                                            }
                                    ))

    context ={
        'form': form,
        'pk': pk,
        'slug': slug,
    }
    return render(request, 'event/register_supportneeded.html', context)


def supportneeded_details(request, pk, slug, support_pk, support_slug):
    supportneeded = get_object_or_404(SupportNeeded, id=support_pk)
    if supportneeded.slug != support_slug:
        return HttpResponsePermanentRedirect(supportneeded.get_absolute_url())

    current_user = request.user

    context = {
        'current_user': current_user,
        'supportneeded': supportneeded,
    }

    return render(request, 'event/supportneeded_details.html', context)


@login_required
def cancel_supportneeded_or_activate_again(request, pk, slug, support_pk, support_slug):
    supportneeded = SupportNeeded.objects.get(pk=support_pk)

    if request.user == supportneeded.event.user:
        if supportneeded.cancelled:
            supportneeded.cancelled = False
        else:
            supportneeded.cancelled = True
        supportneeded.save()

    #Todo: redirect to calling page
    return redirect(reverse('event:supportneeded_details', kwargs={'pk': pk,
                                                                   'slug': slug,
                                                                   'support_pk': support_pk,
                                                                   'support_slug': support_slug,
                                                                   }
                            )
                    )


@login_required
def register_supportoffer(request, pk, slug, support_pk, support_slug):
    form = SupportOfferForm(request.POST or None)
    if form.is_valid():
        user = request.user
        form.cleaned_data['user'] = user
        supportneeded = SupportNeeded.objects.get(pk=support_pk)
        form.cleaned_data['supportneeded'] = supportneeded

        supportoffer = SupportOffer.objects.create(**form.cleaned_data)

        return redirect(reverse('event:supportoffer_details',
                                kwargs={'pk': pk,
                                        'slug': slug,
                                        'support_pk': support_pk,
                                        'support_slug': support_slug,
                                        'offer_pk': supportoffer.pk,
                                        }
                                ))

    context ={
        'form': form,
    }
    return render(request, 'transportation/transportation_request.html', context)


@login_required
def supportoffer_details(request, pk, slug, support_pk, support_slug, offer_pk):
    supportoffer = get_object_or_404(SupportOffer, id=offer_pk)

    current_user = request.user
    user_list = [supportoffer.user, supportoffer.supportneeded.event.user]

    context = {
        'current_user': current_user,
        'supportoffer': supportoffer,
        'user_list': user_list,
    }

    return render(request, 'event/supportoffer_details.html', context)


def cancel_or_reactivate_supportoffer(request, pk, slug, support_pk, support_slug, offer_pk):
    supportoffer = SupportOffer.objects.get(pk=offer_pk)

    if request.user == supportoffer.user:
        if supportoffer.cancelled:
            supportoffer.cancelled = False
        else:
            supportoffer.cancelled = True
        supportoffer.save()

    #Todo: redirect to calling page
    return redirect(reverse('event:supportoffer_details', kwargs={'pk': pk,
                                                                   'slug': slug,
                                                                   'support_pk': support_pk,
                                                                   'support_slug': support_slug,
                                                                    'offer_pk': offer_pk,
                                                                   }))

def search_event(request):
    form = EventSearchForm(request.POST or None)

    if form.is_valid():

        for key, value in form.cleaned_data.items():
            request.session[key] = value

        radius = 25
        request.session['radius'] = radius

        return redirect(reverse('event:view_search_results'))

    context = {
        'form': form,
    }

    return render(request, 'event/search_event.html', context)


def view_search_results(request):
    ''' Prepares form data for querying events  and lists result. '''

    # prepare location
    search_location = request.session.get('location')
    lat = request.session.get('lat')
    long = request.session.get('long')
    distance = request.session.get('radius')
    location = GeoLocation.from_degrees(float(lat), float(long))
    SW_loc, NE_loc = location.bounding_locations(distance)

    # prepare rest
    current_date = datetime.now()

    # prepare query
    lat_max = NE_loc.deg_lat
    lat_min = SW_loc.deg_lat
    long_max = NE_loc.deg_lon
    long_min = SW_loc.deg_lon

    middle_location = (lat, long)
    result = geo_test(middle_location, SW_loc)

    continuing_query = Event.objects.filter(lat__lt=lat_max, lat__gt=lat_min,
                                            long__lt=long_max, long__gt=long_min,
                                            continuing=True,
                                            cancelled=False,
                                            ).order_by('-date')

    event_query = Event.objects.filter(lat__lt=lat_max, lat__gt=lat_min,
                                       long__lt=long_max, long__gt=long_min,
                                       date__gte=current_date,
                                       continuing=False,
                                       cancelled=False,
                                       ).order_by('-date')

    context = {
        'location': search_location,
        'continuing_query': continuing_query,
        'event_query': event_query,
    }

    return render(request, 'event/view_search_event.html', context)