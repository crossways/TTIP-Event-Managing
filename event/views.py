from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import UpdateView

from .models import Event
from .forms import EventForm

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
    return redirect(reverse('transportation:transportation_details', kwargs={'pk': event.pk, 'slug': event.slug}))