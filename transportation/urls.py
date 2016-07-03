from django.conf.urls import include, url

from .views import TransportationOfferUpdate

urlpatterns = [
    url(r'^angebote/(?P<pk>\d+)/(?P<slug>[\w-]+)/$', 'transportation.views.details', name="details"),
    url(r'^angebote/(?P<pk>\d+)/(?P<slug>[\w-]+)/aendern/$', view= TransportationOfferUpdate.as_view(), name="update_transportation"),
    url(r'^angebote/(?P<pk>\d+)/(?P<slug>[\w-]+)/anfrage/$', 'transportation.views.transportation_request', name="transportation_request"),
    url(r'^fahrt_stornieren_oder_einstellen(?P<pk>\d+)/(?P<slug>[\w-]+)$', 'transportation.views.cancel_ride_or_activate_again', name="cancel_or_activate"),
    url(r'^suchen/(?P<pk>\d+)/(?P<slug>[\w-]+)/$', 'transportation.views.search_details', name="search_details"),
    url(r'^$', 'transportation.views.transportation_startingpage', name='transportation_startingpage'),
    url(r'^biete_fahrt_an/$', 'transportation.views.register_transportation_offer', name="register_transportation"),
    url(r'^zwischenstopp_hinzufügen_zu/(?P<pk>\d+)/(?P<slug>[\w-]+)/$', 'transportation.views.add_additional_stops', name="add_additional_stops"),
]