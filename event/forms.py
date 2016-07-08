from django import forms
from django.forms.extras.widgets import SelectDateWidget

from geopy.geocoders import GoogleV3

from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'name',
            'location',
            'other_location',
            'street',
            'zip_code',
            'continuing',
            'date',
            'description',
            'telephone',
            'mobile',
            'email',
            # 'header picture',
            # 'multiple files',
        ]

        help_texts = {
            'name': "z.B Flyer verteilen, Themenwagen bauen, T-Shirts bedrucken, etc.",
            'continuing': "Längerwährend z.B. durch Bauzeit eines Themenwagens",
            'date': "Bei länger währenden Projekten wie Themenwagen bauen: Tag des Projektstarts angeben.\n"
                    "Bei einmaligen Events wie 'Flyer verteilen': Tag und Uhrzeit an dem Flyer verteilt werden.",
        }

        widgets = {
            'date': SelectDateWidget,
        }

    def clean(self):
        choice_location = self.cleaned_data.get('location')
        other_location = self.cleaned_data.get('other_location')
        zip_code = self.cleaned_data.get('zip_code')
        street = self.cleaned_data.get('street')

        if choice_location and other_location:
            raise forms.ValidationError(
                "Füllen Sie bitte entweder 'Stadt mit Großdemo' oder 'Stadt ohne Großdemo' aus."
            )
        if choice_location:
            location = choice_location
        else:
            location = other_location

        geolocator = GoogleV3()
        loc = geolocator.geocode("{} {} {}".format(zip_code, location, street))

        try:
            loc.latitude
            loc_dict = {
                'lat': loc.latitude,
                'long': loc.longitude,
            }
            self.cleaned_data.update(loc_dict)
        except AttributeError:
            raise forms.ValidationError(
                "Event Location konnte nicht gefunden werden. Fehler in der Adresse"
            )