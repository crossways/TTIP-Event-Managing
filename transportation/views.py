from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import render, redirect,get_object_or_404
from django.views.generic.edit import UpdateView

from .forms import TransportationOfferForm, TransportationBreaksForm, TransportationRequestForm
from .models import TransportationOffer, TransportationBreaks, TransportationRequest, TransportationSearch

# Create your views here.

class TransportationOfferUpdate(UpdateView):
    model = TransportationOffer
    form_class = TransportationOfferForm
    template_name = 'transportation/transportation_offer_change.html'

    def form_valid(self, form):
        transportation = self.object
        TransportationOffer.objects.filter(pk=transportation.pk).update(**form.cleaned_data)
        return redirect(
            reverse('transportation:details', kwargs={'pk': transportation.pk, 'slug': transportation.slug}))

    '''
    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk', None)
        form = TransportationOfferForm(request.POST)

        if form.is_valid():
            TransportationOffer.objects.filter(pk=pk).update(**form.cleaned_data)
            transportation = TransportationOffer.objects.get(pk=pk)
            return redirect(
                reverse('transportation:details', kwargs={'pk': transportation.pk, 'slug': transportation.slug}))
        else:
            return self.render_to_response(self.get_context_data(form=form))
    '''

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

    current_user = request.user
    address = "{} {}".format(transportation.lat, transportation.long)
    print("{} {}".format(transportation.lat, transportation.long))
    context = {
        'current_user': current_user,
        'transportation': transportation,
        'address': address,
    }
    return render(request, 'transportation/view_transportation.html', context, )

def cancel_ride_or_activate_again(request, pk, slug):
    transportation = TransportationOffer.objects.get(id=pk)

    if request.user == transportation.user:
        if transportation.cancelled:
            transportation.cancelled = False
        else:
            transportation.cancelled = True
        transportation.save()

    #Todo: redirect to calling page
    return redirect(reverse('transportation:details', kwargs={'pk': transportation.pk, 'slug': transportation.slug}))


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


@login_required
def transportation_request(request, pk, slug):
    form = TransportationRequestForm(request.POST or None)
    if form.is_valid():
        user = request.user
        form.cleaned_data['user'] = user
        transporation_offer = TransportationOffer.objects.get(pk=pk)
        form.cleaned_data['transporation_offer'] = transporation_offer

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


def transportation_request_view(request, pk, slug, request_pk):

    context = {
        'pk': pk,
        'slug': slug,
    }
    return render(request, 'transportation/view_request.html', context)