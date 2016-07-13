from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import UpdateView
import json

from .forms import TransportationOfferForm, TransportationBreaksForm, TransportationRequestForm, TransportationAvailableSeatsForm, TransportationSearchForm
from .models import TransportationOffer, TransportationBreaks, TransportationRequest, TransportationSearch
from .utils.geo import GeoLocation, geo_test
from .utils.radius_correction import add_km_to_radius
from .utils.transportation_extras import date_handler

# Create your views here.

class TransportationOfferUpdate(UpdateView):
    model = TransportationOffer
    form_class = TransportationOfferForm
    template_name = 'transportation/transportation_offer_change.html'

    def form_valid(self, form):
        transportation = self.object
        TransportationOffer.objects.filter(pk=transportation.pk).update(**form.cleaned_data)
        return redirect(
            reverse('transportation:transportation_details', kwargs={'pk': transportation.pk, 'slug': transportation.slug}))


class TransportationRequestUpdate(UpdateView):
    model = TransportationRequest
    form_class = TransportationRequestForm
    template_name = 'transportation/change_request.html'


def transportation_startingpage(request):
    return render(request, 'transportation/starting_page.html')


def details(request, pk, slug):
    # try... to delete session trans_pk which made sure user does not register same ride two times
    try:
        request.session.pop('trans_pk')
    except KeyError:  # Todo: Check if this is the right Error for not existing trans_pk
        pass

    transportation = get_object_or_404(TransportationOffer, id=pk)
    if transportation.slug != slug:
        return HttpResponsePermanentRedirect(transportation.get_absolute_url())

    transportation_request = TransportationRequest.objects.filter(transporation_offer=transportation.pk)
    current_user = request.user
    address = "{} {}".format(transportation.lat, transportation.long)
    #passengers = {request.user:request.pk for request in transportation_request}

    context = {
        'current_user': current_user,
        'transportation': transportation,
        'transportation_request': transportation_request,
        'address': address,
    }
    if current_user in [request.user for request in transportation_request]:
        current_user_requests = transportation_request.filter(user=current_user)
        context.update({'current_user_requests': current_user_requests})

    return render(request, 'transportation/view_transportation.html', context, )

@login_required
def cancel_ride_or_activate_again(request, pk, slug):
    transportation = TransportationOffer.objects.get(id=pk)

    if request.user == transportation.user:
        if transportation.cancelled:
            transportation.cancelled = False
        else:
            transportation.cancelled = True
        transportation.save()

    #Todo: redirect to calling page
    return redirect(reverse('transportation:transportation_details', kwargs={'pk': transportation.pk, 'slug': transportation.slug}))


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


''' Ausgeklammert für später. redirects to additional_stops
@login_required
def register_transportation_offer(request):
    form = TransportationOfferForm(request.POST or None)

    if form.is_valid():
        user = request.user
        form.cleaned_data['user'] = user
        transportation_id_in_session = request.session.get('trans_pk', '')
        #transportation_exist = TransportationOffer.objects.get(pk=request.session.get('trans_pk', ''))
        if transportation_id_in_session:
            TransportationOffer.objects.filter(pk=transportation_id_in_session).update(**form.cleaned_data)
            transportation = TransportationOffer.objects.get(pk=transportation_id_in_session)
        else:
            transportation = TransportationOffer.objects.create(**form.cleaned_data)
            request.session['trans_pk'] = transportation.pk
        return redirect(reverse('transportation:add_additional_stops', kwargs={'pk': transportation.pk, 'slug': transportation.slug}))

    context = {
        'form': form,
    }

    return render(request, 'transportation/register_transportation_offer.html', context)
'''

@login_required
def register_transportation_offer(request):
    form = TransportationOfferForm(request.POST or None)

    if form.is_valid():
        user = request.user
        form.cleaned_data['user'] = user

        transportation = TransportationOffer.objects.create(**form.cleaned_data)

        return redirect(
            reverse('transportation:transportation_details',
                    kwargs={'pk': transportation.pk, 'slug': transportation.slug}))

    context = {
        'form': form,
    }

    return render(request, 'transportation/register_transportation_offer.html', context)


@login_required
def add_additional_stops(request, pk, slug):
    current_user = request.user
    transportation = get_object_or_404(TransportationOffer, id=pk)
    if request.user != transportation.user:
        return redirect(
            reverse('transportation:transportation_details', kwargs={'pk': transportation.pk, 'slug': transportation.slug}))

    form = TransportationBreaksForm(request.POST or None)
    if form.is_valid():
        new_break = TransportationBreaks.objects.create(**form.cleaned_data)
        transportation.breaks.add(new_break)

        return redirect(
            reverse('transportation:transportation_details', kwargs={'pk': transportation.pk, 'slug': transportation.slug}))

    context = {
        'form': form,
        'current_user': current_user,
        'transportation': transportation,
    }
    return render(request, 'transportation/add_additional_stops.html', context)


@login_required
def change_available_seats(request, pk, slug):
    form = TransportationAvailableSeatsForm(request.POST or None)
    transportation = TransportationOffer.objects.get(pk=pk)
    current_user = request.user
    if form.is_valid():
        new_seats = form.cleaned_data.get('seats_available')
        if new_seats >= 0:
            transportation.seats_available = new_seats
            transportation.save()
        return redirect(reverse('transportation:transportation_details',
                                kwargs={'pk': transportation.pk,
                                        'slug': transportation.slug,
                                        }
                                ))

    context = {
        'form': form,
        'current_user': current_user,
        'transportation': transportation,
    }

    return render(request, 'transportation/change_available_seats.html', context)

@login_required
def transportation_request_on_offer(request, pk, slug):
    ''' Creates an request for an existing TransportationOffer object '''
    form = TransportationRequestForm(request.POST or None)
    if form.is_valid():
        user = request.user
        form.cleaned_data['user'] = user
        transportation_offer = TransportationOffer.objects.get(pk=pk)
        form.cleaned_data['transporation_offer'] = transportation_offer

        transportation_request_id = request.session.get('trans_request_pk', '')
        if transportation_request_id:
            TransportationRequest.objects.filter(pk=transportation_request_id).update(**form.cleaned_data)
            transportation_request = TransportationRequest.objects.get(pk=transportation_request_id)
        else:
            transportation_request = TransportationRequest.objects.create(**form.cleaned_data)
            request.session['trans_request_pk'] = transportation_request.pk
        return redirect(reverse('transportation:transportation_request_view',
                                kwargs={'pk': transportation_request.transporation_offer.pk,
                                        'slug': transportation_request.transporation_offer.slug,
                                        'request_pk': transportation_request.pk}
                                ))

    context ={
        'form': form,
    }
    return render(request, 'transportation/transportation_request.html', context)

@login_required
def transportation_request_view(request, pk, slug, request_pk):
    transportation = TransportationOffer.objects.get(pk=pk)
    transportation_request = TransportationRequest.objects.get(pk=request_pk)
    transportation_user = transportation.user
    current_user = request.user
    user_list = [transportation_request.user, transportation_user,]

    if current_user == transportation_user:
        if not transportation_request.seen:
            transportation_request.seen = True
            transportation_request.save()

    context = {
        'transportation': transportation,
        'transportation_request': transportation_request,
        'user': current_user,
        'user_list': user_list,
    }
    return render(request, 'transportation/view_request.html', context)

@login_required
def accept_or_oposite_request(request, pk, slug, request_pk):
    transportation = TransportationOffer.objects.get(id=pk)
    transportation_request = TransportationRequest.objects.get(pk=request_pk)
    passengers = transportation_request.passengers

    if request.user == transportation.user:
        if transportation_request.accepted_by_receiver:
            transportation_request.accepted_by_receiver = False
            if not transportation_request.cancelled:
                transportation.increase_seats(passengers)
        else:
            if not transportation_request.cancelled:
                transportation_request.accepted_by_receiver = True
                # eingefügt
                if passengers > transportation.seats_available:
                    return redirect('transportation:to_much_passengers')
                else:
                    transportation.decrease_seats(passengers)
        transportation.save()
        transportation_request.save()


    return redirect(reverse('transportation:transportation_request_view', kwargs={
        'pk': pk,
        'slug': slug,
        'request_pk': request_pk,
    }
                    ))


def to_much_passengers(request):
    return render(request, 'transportation/to_many_passengers.html')


@login_required
def cancel_or_reactivate_request(request, pk, slug, request_pk):
    transportation = TransportationOffer.objects.get(id=pk)
    transportation_request = TransportationRequest.objects.get(pk=request_pk)
    passengers = transportation_request.passengers

    if request.user == transportation_request.user:
        if transportation_request.cancelled:
            transportation_request.cancelled = False
            if transportation_request.accepted_by_receiver:
                # eingefügt
                if passengers > transportation.seats_available:
                    return redirect('transportation:to_much_passengers')
                else:
                    transportation.decrease_seats(passengers)
        else:
            transportation_request.cancelled = True
            if transportation_request.accepted_by_receiver:
                transportation.increase_seats(passengers)
        transportation.save()
        transportation_request.save()

    return redirect(reverse('transportation:transportation_request_view', kwargs={
        'pk': pk,
        'slug': slug,
        'request_pk': request_pk,
    }
                    ))


def transportation_search_form(request):
    ''' View template with form to fill in query information to find transportation_offers. '''

    form = TransportationSearchForm(request.POST or None)

    if form.is_valid():
        date = form.cleaned_data.get('date')
        date = json.dumps(date, default=date_handler)
        form.cleaned_data['date'] = date

        old_radius = form.cleaned_data.get('radius')
        departure_location = form.cleaned_data.get('departure_location')
        radius = add_km_to_radius(int(old_radius), departure_location)

        for key, value in form.cleaned_data.items():
            request.session[key] = value

        request.session['radius'] = radius

        return redirect(reverse('transportation:view_search_results'))

    context = {
        'form': form,
    }
    return render(request, 'transportation/search_transportation.html', context)


def view_search_results(request):
    ''' Prepares form data for querying transportation offers and lists result. '''

    # prepare startlocation
    lat = request.session.get('lat')
    long = request.session.get('long')
    distance = request.session.get('radius')
    location = GeoLocation.from_degrees(float(lat), float(long))
    SW_loc, NE_loc = location.bounding_locations(distance)

    # prepare endlocation
    destiny_lat =  request.session.get('destiny_lat')
    destiny_long = request.session.get('destiny_long')
    destiny_location = GeoLocation.from_degrees(float(destiny_lat), float(destiny_long))
    destiny_SW_loc, destiny_NE_loc = destiny_location.bounding_locations(18)

    # prepare rest
    passengers = request.session.get('passengers')
    demo_city = request.session.get('destiny_location')

    # prepare query
    lat_max = NE_loc.deg_lat
    lat_min = SW_loc.deg_lat
    long_max = NE_loc.deg_lon
    long_min = SW_loc.deg_lon

    dest_lat_max = destiny_NE_loc.deg_lat
    dest_lat_min = destiny_SW_loc.deg_lat
    dest_long_max = destiny_NE_loc.deg_lon
    dest_long_min = destiny_SW_loc.deg_lon

    #middle_location = (lat, long)
    #result = geo_test(middle_location, SW_loc)

    offer_query = TransportationOffer.objects.filter(lat__lt=lat_max, lat__gt=lat_min,
                                                     long__lt=long_max, long__gt=long_min,
                                                     destiny_lat__lt=dest_lat_max, destiny_lat__gt= dest_lat_min,
                                                     destiny_long__lt=dest_long_max, destiny_long__gt=dest_long_min,
                                                     seats_available__gte=passengers,
                                                     cancelled=False,
                                                     ).order_by('-departure')

    context = {
        'destiny_location': demo_city,
        'offer_query': offer_query,
    }

    return render(request, 'transportation/view_search_result.html', context)
