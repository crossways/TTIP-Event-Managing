from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import UpdateView

from .models import Event, SupportNeeded, SupportOffer
from .forms import EventForm, SupportNeededForm

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
    address = "{} {}".format(event.lat, event.long)

    context = {
        'current_user': current_user,
        'event': event,
        'address': address,
    }

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


'''
@login_required
def register_supportoffer(request, pk, slug):
    form = SupportNeededForm(request.POST or None)
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
'''