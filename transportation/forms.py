from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Fieldset, ButtonHolder
from crispy_forms.bootstrap import FormActions
from django import forms

from geopy.geocoders import GoogleV3

from .models import TransportationBreaks, TransportationOffer


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
            'additional_breaks',
        ]

        help_texts = {
            'departure': 'Gebe eine kurze Beschreibung der negativen Wirkung hier ein',
        }



    def clean(self):
        # departure
        departure_location = self.cleaned_data.get('departure_location')
        zip_code = str(self.cleaned_data.get('zip_code'))
        departure_street = self.cleaned_data.get('departure_street')
        # destiny
        destiny_location = self.cleaned_data.get('destiny_location')
        destiny_zip_code = str(self.cleaned_data.get('destiny_zip_code'))
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
                'destiny_long': departure_loc.longitude,
            }
            self.cleaned_data.update(destiny_dict)
        except AttributeError:
            raise forms.ValidationError(
                "Leider ist ein Fehler in der Zielortadresse."
            )

    '''
    def __init__(self, *args, **kwargs):
        super(TransportationOfferForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
                        Fieldset(
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
                            'additional_breaks',
                        ),
                        FormActions(
                            Submit('submit', 'Record', css_class='btn btn-primary'),
                            )
                        )'''
