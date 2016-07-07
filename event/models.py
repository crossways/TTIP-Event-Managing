from django.conf import settings
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
    location = models.CharField(max_length=50, choices=CITIES , verbose_name="Stadt")
    street = models.CharField(max_length=50, blank=True, choices=CITIES , verbose_name="Straße")
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
    vacancy = models.CharField(max_length=100, verbose_name="Aufgabengebiet / Berufsbezeichnung")
    description = models.TextField(blank=True, max_length=300, verbose_name="Beschreibung")
    cancelled = models.BooleanField(default=False, verbose_name='Gelöscht')
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)


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
