from django.conf.urls import include, url

from .views import TransportationOfferUpdate

urlpatterns = [
    url(r'^angebote/(?P<pk>\d+)/(?P<slug>[\w-]+)/$', 'transportation.views.details', name="details"),
    url(r'^angebote/(?P<pk>\d+)/(?P<slug>[\w-]+)/aendern/$', view= TransportationOfferUpdate.as_view(), name="update_transportation"),
    url(r'^suchen/(?P<pk>\d+)/(?P<slug>[\w-]+)/$', 'transportation.views.search_details', name="search_details"),
    url(r'^$', 'transportation.views.transportation_startingpage', name='transportation_startingpage'),
    url(r'^biete_fahrt_an/$', 'transportation.views.register_transportation_offer', name="register_transportation"),
    url(r'^zwischenstopp_hinzufügen_zu/(?P<pk>\d+)/(?P<slug>[\w-]+)/$', 'transportation.views.add_additional_stops', name="add_additional_stops"),
]