from django.contrib import admin
from .models import TransportationBreaks, TransportationOffer, TransportationRequest, TransportationSearch

admin.site.register(TransportationBreaks)
admin.site.register(TransportationRequest)
admin.site.register(TransportationSearch)



class TransportationRequestInline(admin.TabularInline):
    model = TransportationRequest
    extra = 1


class TransportationOfferAdmin(admin.ModelAdmin):
    inlines = (TransportationRequestInline, )

admin.site.register(TransportationOffer, TransportationOfferAdmin)