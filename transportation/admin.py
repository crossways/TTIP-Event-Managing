from django.contrib import admin
from .models import TransportationBreaks, TransportationOffer, TransportationRequest, TransportationSearch

admin.site.register(TransportationBreaks)
admin.site.register(TransportationOffer)
admin.site.register(TransportationRequest)
admin.site.register(TransportationSearch)
