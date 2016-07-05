from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import F
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.shortcuts import redirect

# Create your models here.

class TransportationSearch(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Benutzer")
    passengers = models.PositiveIntegerField(verbose_name="Mitfahrer insgesamt")
    location = models.CharField(max_length=50, verbose_name="Ort")
    zip_code = models.CharField(max_length=5, verbose_name="Postleitzahl")
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
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Fahrtsuche"
        verbose_name_plural = "Fahrtsuchen"

    def get_absolute_url(self):
        return reverse('transportation:details_search', kwargs={'pk': str(self.pk), 'slug': self.slug})


class TransportationBreaks(models.Model):
    location = models.CharField(max_length=50, verbose_name="Ort")
    street = models.CharField(max_length=70, verbose_name="Straße")
    zip_code = models.CharField(max_length=5, verbose_name="Postleitzahl")
    price = models.FloatField(null=True, blank=True, verbose_name="Preis in Euro")
    rank = models.PositiveIntegerField(verbose_name="Haltenummer")
    lat = models.FloatField(verbose_name="Latitude")
    long = models.FloatField(verbose_name="Longitude")
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

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
    zip_code = models.CharField(max_length=5, verbose_name="Postleitzahl Abfahrtsort")
    departure_street = models.CharField(max_length=70, verbose_name="Straße Abfahrtsort")
    departure = models.DateTimeField(verbose_name="Abfahrtstag und Zeit")
    lat = models.FloatField(verbose_name="Latitude")
    long = models.FloatField(verbose_name="Longitude")
    destiny_location = models.CharField(max_length=50, verbose_name="Zielort")
    destiny_zip_code = models.CharField(max_length=5, verbose_name="Postleitzahl Zielort")
    destiny_street = models.CharField(max_length=70, verbose_name="Straße Zielort")
    destiny_lat = models.FloatField(verbose_name="Latitude")
    destiny_long = models.FloatField(verbose_name="Longitude")
    mobile = models.CharField(max_length=20, blank=True, verbose_name="Mobilnummer")
    price = models.FloatField(null=True, blank=True, verbose_name="Preis in Euro")
    cancelled = models.BooleanField(default=False, verbose_name='Fahrt storniert')

    additional_breaks = models.BooleanField(default=False, verbose_name="Ungeplante Zwischenstopps möglich?") # Request should have additional function, where people can find drivers,
                                                # who are headding to their hometown. Breaks=True would show them they could ask for additional stop
    breaks = models.ManyToManyField(TransportationBreaks)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Fahrtangebot"
        verbose_name_plural = "Fahrtangebote"

    def __str__(self):
        return "{}: Von {} nach {}.".format(self.user, self.departure_location, self.destiny_location)

    def get_absolute_url(self):
        return reverse('transportation:transportation_details', kwargs={'pk': str(self.pk), 'slug': self.slug})

    def increase_seats(self, seats):
        self.seats_available += seats

    def decrease_seats(self, seats):
        if seats > self.seats_available:
            return redirect('transportation:to_much_passengers')
        else:
            self.seats_available -= seats


class TransportationRequest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Benutzer")
    transporation_offer = models.ForeignKey(TransportationOffer, blank=True, null=True)
    transporation_break = models.ForeignKey(TransportationBreaks, blank=True, null=True)
    passengers = models.PositiveIntegerField(verbose_name="Mitfahrer insgesamt")
    text = models.TextField(max_length=800, blank=True, verbose_name="Nachricht")
    mobile = models.CharField(max_length=20, blank=True, verbose_name="Mobilnummer")
    accepted_by_receiver = models.BooleanField(default=False, verbose_name="Anfrage akzeptieren.")
    denied_by_reveicer = models.BooleanField(default=False, verbose_name="Anfrage ablehnen.")
    cancelled = models.BooleanField(default=False, verbose_name="Anfrage stornieren/ablehnen.")
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name = "Fahrtanfrage"
        verbose_name_plural ="Fahrtanfragen"

    def __str__(self):
        return "Anfrage von {}: Start {} nach {}. {}".format(self.user, self.transporation_offer.departure_location, self.transporation_offer.destiny_location, self.transporation_offer.departure)

    def get_absolute_url(self):
        return reverse('transportation:transportation_request_view', kwargs={'pk': str(self.transporation_offer.pk),
                                                         'slug': self.transporation_offer.slug,
                                                         'request_pk': self.pk})


def prepare_string(instance, var):
    replacements = [(u'ä', u'ae'), (u'ö', u'oe'), (u'ü', u'ue'), (u'ß', u'sz'), ]
    destiny_location = instance.destiny_location
    for (s, r) in replacements:
        var = var.replace(s, r)
        destiny_location = destiny_location.replace(s, r)

    return destiny_location, var


def create_slug(instance, new_slug=None):

    if hasattr(instance, 'departure_location'):
        var = instance.departure_location
        destiny_location, var = prepare_string(instance, var)
        string = "von {} nach {}".format(var, destiny_location)
    else:
        var = instance.departure
        destiny_location, var = prepare_string(instance, var)
        string = "{} nach {}".format(var, destiny_location)

    slug = slugify(string)
    if new_slug is not None:
        slug = new_slug
    qs = TransportationOffer.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)

    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not slugify(instance.departure_location) in instance.slug\
            or not slugify(instance.destiny_location) in instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, sender=TransportationOffer)
pre_save.connect(pre_save_post_receiver, sender=TransportationSearch)