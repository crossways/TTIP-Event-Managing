from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Fieldset, ButtonHolder
from crispy_forms.bootstrap import FormActions
from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import SplitDateTimeWidget

from datetime import datetime
from geopy.geocoders import GoogleV3
import pytz


from .models import TransportationBreaks, TransportationOffer, TransportationRequest
from .utils.geo import geo_lat_long_eval

class TransportationOfferForm(forms.ModelForm):
    class Meta:
        model = TransportationOffer
        fields = [
            'company',
            'car_manufacturer',
            'car_model',
            'seats_available',
            'departure_location',
            'zip_code',
            'departure_street',
            'departure',
            'destiny_location',
            'destiny_zip_code',
            'destiny_street',
            'price',
            'mobile',
            #'additional_breaks',
        ]

        help_texts = {
            'departure': "Erstes Feld: Datum (tt.mm.jj). Zweites Feld: Uhrzeit (Eingabebeispiel: 17:00)"
        }

        widgets = {
            'departure': SplitDateTimeWidget,
        }

    def clean(self):
        date = self.cleaned_data.get('departure')
        utc = pytz.UTC
        now = utc.localize(datetime.now())
        # departure
        departure_location = self.cleaned_data.get('departure_location')
        zip_code = self.cleaned_data.get('zip_code')
        departure_street = self.cleaned_data.get('departure_street')
        # destiny
        destiny_location = self.cleaned_data.get('destiny_location')
        destiny_zip_code = self.cleaned_data.get('destiny_zip_code')
        destiny_street = self.cleaned_data.get('destiny_street')

        geolocator = GoogleV3()
        departure_loc = geolocator.geocode("{} {} {}".format(zip_code, departure_location, departure_street))
        destiny_loc = geolocator.geocode("{} {} {}".format(destiny_zip_code, destiny_location, destiny_street))

        try:
            departure_loc.latitude
            departure_dict = {
                'lat': departure_loc.latitude,
                'long': departure_loc.longitude,
            }
            self.cleaned_data.update(departure_dict)
        except AttributeError:
            raise forms.ValidationError(
                "Leider ist ein Fehler in der Abfahrtsortadresse."
            )

        try:
            destiny_loc.latitude
            destiny_dict = {
                'destiny_lat': destiny_loc.latitude,
                'destiny_long': destiny_loc.longitude,
            }
            self.cleaned_data.update(destiny_dict)
        except AttributeError:
            raise forms.ValidationError(
                "Leider ist ein Fehler in der Zielortadresse."
            )

        if date < datetime(2016, 9, 16, tzinfo=utc) or date > datetime(2016, 9, 19, tzinfo=utc):
            raise forms.ValidationError(
                "Bitte nur Fahrten im Zeitraum der Großdemonstrationen anbieten! Möglicher Zeitraum: 16.09 bis 18.09.2016."
            )



class TransportationAvailableSeatsForm(forms.ModelForm):
    class Meta:
        model = TransportationOffer
        fields = [
            'seats_available'
        ]


class TransportationBreaksForm(forms.ModelForm):
    class Meta:
        model = TransportationBreaks
        fields = [
            'location',
            'street',
            'zip_code',
            'price',
            'rank',
        ]
        help_texts = {
            'rank': 'Um den wievielten Stopp auf der Route handelt es sich?',
        }

    def clean(self):
        location = self.cleaned_data.get('location')
        zip_code = str(self.cleaned_data.get('zip_code'))
        street = self.cleaned_data.get('street')

        geolocator = GoogleV3()
        loc = geolocator.geocode("{} {} {}".format(zip_code, location, street))
        try:
            loc.latitude
            dict_ = {
                'lat': loc.latitude,
                'long': loc.longitude,
            }
            self.cleaned_data.update(dict_)
        except AttributeError:
            raise forms.ValidationError(
                "Leider ist ein Fehler in der Zwischenstoppadresse."
            )


class TransportationRequestForm(forms.ModelForm):
    class Meta:
        model = TransportationRequest
        fields = [
            'passengers',
            'text',
            'mobile',
        ]

class TransportationSearchForm(forms.Form):
    RADIUS_DISTANCE = (
        (1, 0),
        (5, 5),
        (10, 10),
        (15, 15),
        (20, 20),
        (25, 25),
        (30, 30),
        (40, 40),
        (50, 50),
    )

    departure_location = forms.CharField(max_length=50, label='Abfahrtsort')
    zip_code = forms.CharField(max_length=5, required=False,
                               label='Abfahrtsort Postleitzahl',
                               help_text='Bei kleineren Ortschaften bitte Postleitzahl mit angeben.'
                               )

    destiny_location = forms.CharField(max_length=50, label='Zielort')
    destiny_zip_code = forms.CharField(max_length=5, required=False,
                                       label='Zielort Postleitzahl',
                                       help_text='Bei kleineren Ortschaften bitte Postleitzahl mit angeben.'
                                       )

    passengers = forms.IntegerField(label="Mitfahrer insgesamt")
    radius = forms.ChoiceField(label="Umkreis in km", choices=RADIUS_DISTANCE)
    # date = forms.DateField(label='Datum', widget=SelectDateWidget)

    def clean(self):
        data, boolean = geo_lat_long_eval(self.cleaned_data)
        passengers = self.cleaned_data.get('passengers')

        if boolean:
            self.cleaned_data.update(data)
        else:
            raise forms.ValidationError(
                "{}".format(data)
            )

        if not passengers or passengers < 1:
            raise forms.ValidationError(
                "Mitfahrer muss mindestens 1 sein."
            )