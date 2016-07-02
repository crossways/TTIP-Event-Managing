from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import F

# Create your models here.

class TransportationRequest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Benutzer")
    passengers = models.PositiveIntegerField(verbose_name="Mitfahrer insgesamt")
    location = models.CharField(max_length=50, verbose_name="Ort")
    zip_code = models.PositiveIntegerField(verbose_name="Postleitzahl")
    street = models.CharField(max_length=70, blank=True, verbose_name="Straße")
    lat = models.FloatField(verbose_name="Latitude")
    long = models.FloatField(verbose_name="Longitude")
    radius = models.PositiveIntegerField(verbose_name="Umkreis")
    departure = models.DateField(verbose_name="Reisetag")
    destiny_location = models.CharField(max_length=50)
    destiny_zip_code = models.PositiveIntegerField(verbose_name="Postleitzahl Zielort")
    destiny_lat = models.FloatField(verbose_name="Latitude")
    destiny_long = models.FloatField(verbose_name="Longitude")
    mobile = models.CharField(max_length=20, blank=True, verbose_name="Mobilnummer")

    class Meta:
        verbose_name = "Fahrtanfrage"
        verbose_name_plural = "Fahrtanfragen"


class TransportationBreaks(models.Model):
    location = models.CharField(max_length=50, verbose_name="Ort")
    street = models.CharField(max_length=70, verbose_name="Straße")
    zip_code = models.PositiveIntegerField(verbose_name="Postleitzahl")
    price = models.FloatField(null=True, blank=True, verbose_name="Preis in Euro")
    rank = models.PositiveIntegerField(verbose_name="Haltenummer")
    lat = models.FloatField(verbose_name="Latitude")
    long = models.FloatField(verbose_name="Longitude")

    class Meta:
        verbose_name = "Zwischenstopp"
        verbose_name_plural = "Zwischenstopps"

    def __str__(self):
        return self.location


class TransportationOffer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Benutzer")
    company = models.BooleanField(default=False, verbose_name="Angebot eines Transportunternehmens?")
    car_manufacturer = models.CharField(max_length=20, verbose_name="Automarke")
    car_model = models.CharField(max_length=20, verbose_name="Automodell")
    seats_available = models.PositiveIntegerField(verbose_name="Freie Sitzplätze")
    departure_location = models.CharField(max_length=50, verbose_name="Abfahrtsort")
    zip_code = models.PositiveIntegerField(verbose_name="Postleitzahl Abfahrtsort")
    departure_street = models.CharField(max_length=70, verbose_name="Straße Abfahrtsort")
    departure = models.DateTimeField(verbose_name="Abfahrtstag und Zeit")
    lat = models.FloatField(verbose_name="Latitude")
    long = models.FloatField(verbose_name="Longitude")
    destiny_location = models.CharField(max_length=50, verbose_name="Zielort")
    destiny_zip_code = models.PositiveIntegerField(verbose_name="Postleitzahl Zielort")
    destiny_street = models.CharField(max_length=70, verbose_name="Straße Zielort")
    destiny_lat = models.FloatField(verbose_name="Latitude")
    destiny_long = models.FloatField(verbose_name="Longitude")
    mobile = models.CharField(max_length=20, blank=True, verbose_name="Mobilnummer")
    price = models.FloatField(null=True, blank=True, verbose_name="Preis in Euro")

    additional_breaks = models.BooleanField(default=False, verbose_name="Ungeplante Zwischenstopps möglich?") # Request should have additional function, where people can find drivers,
                                                # who are headding to their hometown. Breaks=True would show them they could ask for additional stop
    breaks = models.ManyToManyField(TransportationBreaks)

    class Meta:
        verbose_name = "Fahrtangebot"
        verbose_name_plural = "Fahrtangebote"

    def __str__(self):
        return self.destiny_location

    def get_absolute_url(self):
        return reverse('transportation:details', kwargs={'pk': str(self.pk), 'slug': self.slug})

    def increase_seats(self, seats):
        TransportationOffer.objects \
            .filter(pk=self.pk) \
            .update(seats_available=F('seats_available') + seats)

    def decrease_seats(self, seats):
        TransportationOffer.objects \
            .filter(pk=self.pk, likes_count__gt=0) \
            .update(seats_available=F('seats_available') - seats)