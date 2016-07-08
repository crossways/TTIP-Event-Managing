from django.contrib import admin

from .models import Event, SupportNeeded, SupportOffer
# Register your models here.

admin.site.register(Event)
admin.site.register(SupportNeeded)
admin.site.register(SupportOffer)
