from django.contrib import admin
from .models import TransportationBreaks, TransportationOffer, TransportationRequest

admin.site.register(TransportationBreaks)
admin.site.register(TransportationOffer)
admin.site.register(TransportationRequest)
