from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import F
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _


# Create your models here.

CITIES = (
    ('Berlin', 'Berlin'),
    ('Frankfurt', 'Frankfurt'),
    ('Hamburg', 'Hamburg'),
    ('Köln', 'Köln'),
    ('Leipzig', 'Leipzig'),
    ('München', 'München'),
    ('Stuttgart', 'Stuttgart'),
)

class Event(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Benutzer")
    name = models.CharField(max_length=50, verbose_name="Bezeichnung")
    location = models.CharField(max_length=50, choices=CITIES, blank=True, verbose_name="Stadt mit Großdemo")
    other_location = models.CharField(max_length=50, blank=True, verbose_name="Stadt ohne Großdemo")
    zip_code = models.CharField(max_length=5, blank=True, verbose_name="Postleitzahl")
    street = models.CharField(max_length=50, blank=True, verbose_name="Straße")
    lat = models.FloatField(verbose_name="Latitude")
    long = models.FloatField(verbose_name="Longitude")
    date = models.DateTimeField(verbose_name="Veranstaltungstag und Zeit")
    continuing = models.BooleanField(default=False, verbose_name="Längerwährendes Projekt")
    description = models.TextField(blank=True, max_length=1000, verbose_name="Beschreibung")
    telephone = models.CharField(max_length=20, blank=True, verbose_name="Festnetznummer")
    mobile = models.CharField(max_length=20, blank=True, verbose_name="Mobilnummer")
    email = models.CharField(max_length=50, blank=True, verbose_name="Email")
    # header picture            files
    # multiple files
    likes_count = models.PositiveIntegerField(_("likes count"), default=0)
    cancelled = models.BooleanField(default=False, verbose_name='Event storniert')
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def __str__(self):
        return "{} am {}.".format(self.name, self.date)

    def get_absolute_url(self):
        return reverse('event:event_details', kwargs={'pk': self.pk, 'slug': self.slug})

    def increase_likes_count(self):
        Event.objects \
            .filter(pk=self.pk) \
            .update(likes_count=F('likes_count') + 1)

    def decrease_likes_count(self):
        Event.objects \
            .filter(pk=self.pk, likes_count__gt=0) \
            .update(likes_count=F('likes_count') - 1)


class SupportNeeded(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Benutzer")
    event = models.ForeignKey(Event)
    vacancy = models.CharField(max_length=30, verbose_name="Aufgabengebiet / Berufsbezeichnung")
    short_text = models.CharField(max_length=100, verbose_name="Kurzbeschreibung")
    description = models.TextField(blank=True, max_length=1000, verbose_name="Beschreibung")
    cancelled = models.BooleanField(default=False, verbose_name='Gelöscht')
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name = "Hilfsgesuch"
        verbose_name_plural = "Hilfsgesuche"

    def __str__(self):
        return "Gesuch für {} von {}.".format(self.event, self.event.user)


class SupportOffer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Benutzer")
    supportneeded = models.ForeignKey(SupportNeeded)
    text = models.TextField(max_length=800, blank=True, verbose_name="Nachricht")
    mobile = models.CharField(max_length=20, blank=True, verbose_name="Mobilnummer")
    cancelled = models.BooleanField(default=False, verbose_name="Angebot stornieren/ablehnen.")
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name = "Hilfsangebot"
        verbose_name_plural = "Hilfsangebote"

    def __str__(self):
        return "Angebot von {}.".format(self.user)

    def get_absolute_url(self):
        return reverse('event:event_offer_view', kwargs={'pk': str(self.event.pk),
                                                                             'slug': self.event.slug,
                                                                             'request_pk': self.pk})


def create_slug(instance, new_slug=None):
    replacements = [(u'ä', u'ae'), (u'ö', u'oe'), (u'ü', u'ue'), (u'ß', u'sz'),]
    name = instance.name
    for (s, r) in replacements:
        name = name.replace(s, r)

    slug = slugify(name)
    if new_slug is not None:
        slug = new_slug
    qs = Event.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)

    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not slugify(instance.name) in instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, sender=Event)
