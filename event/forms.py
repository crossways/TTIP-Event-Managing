from django import forms
from django.forms.extras.widgets import SelectDateWidget

from geopy.geocoders import GoogleV3

from .models import Event, SupportNeeded, SupportOffer

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

class SupportNeededForm(forms.ModelForm):
    class Meta:
        model = SupportNeeded
        fields = [
            'name',
            'short_text',
            'description',
        ]
        help_texts = {
            'name': "z.B. Flyerverteiler, Tischler, Programmierer, etc.",
            'short_text': "Eine kurze Beschreibung/Bezeichnung. Diese wird in der Präsentationsbox auf deiner Event Seite angezeigt.",
            'description': "Eine ausführliche Beschreibung. Diese wird auf der Gesuch Seite angezeigt.",
        }


class SupportOfferForm(forms.ModelForm):
    class Meta:
        model = SupportOffer
        fields = [
            'mobile',
        ]


class EventSearchForm(forms.Form):
    location = forms.CharField(max_length=50, label='Ort')
    zip_code = forms.CharField(max_length=5, required=False,
                               label='Postleitzahl',
                               help_text='Bei kleineren Ortschaften bitte Postleitzahl mit angeben.'
                               )

    def clean(self):
        geolocator = GoogleV3()
        location = self.cleaned_data.get('location')
        zip_code = self.cleaned_data.get('zip_code')
        loc = geolocator.geocode("{} {}".format(zip_code, location))

        try:
            lat = loc.latitude
            long = loc.longitude
            add_dict = {
                'lat': lat,
                'long': long,
            }
            self.cleaned_data.update(add_dict)
        except AttributeError:
            raise forms.ValidationError(
                "Fehler in der Adresse"
            )