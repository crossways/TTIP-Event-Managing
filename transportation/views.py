from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponsePermanentRedirect

from .forms import TransportationOfferForm
from .models import TransportationOffer

# Create your views here.

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


def transportation_startingpage(request):
    return render(request, 'transportation/starting_page.html')


@login_required
def register_transportation_offer(request):
    form = TransportationOfferForm(request.POST or None)

    if form.is_valid():
        form.cleaned_data['user'] = request.user
        obj = TransportationOffer.objects.create(**form.cleaned_data)


    context = {
        'form': form,
    }

    return render(request, 'transportation/register_transportation_offer.html', context)