from django.conf.urls import include, url

from .views import TransportationOfferUpdate, TransportationRequestUpdate

urlpatterns = [
    url(r'^angebote/(?P<pk>\d+)/(?P<slug>[\w-]+)/aendern/$', view= TransportationOfferUpdate.as_view(), name="update_transportation"),
    url(r'^angebote/(?P<pk>\d+)/(?P<slug>[\w-]+)/anfrage/$', 'transportation.views.transportation_request_on_offer', name="transportation_request"),
    url(r'^angebote/(?P<pk>\d+)/(?P<slug>[\w-]+)/verfuegbare_sitzplaetze/$', 'transportation.views.change_available_seats', name="change_available_seats"),
    url(r'^fahrt_stornieren_oder_einstellen(?P<pk>\d+)/(?P<slug>[\w-]+)$', 'transportation.views.cancel_ride_or_activate_again', name="cancel_or_activate"),
    url(r'^suchen/$', 'transportation.views.transportation_search_form', name="transportation_search_form"),
    url(r'^suchen/ergebnisse/$', 'transportation.views.view_search_results', name="view_search_results"),
    url(r'^anfrage/(?P<pk>\d+)/(?P<slug>[\w-]+)/(?P<request_pk>\d+)/annehmen$', 'transportation.views.accept_or_oposite_request', name="accept_or_oposite_request"),
    url(r'^anfrage/(?P<pk>\d+)/(?P<slug>[\w-]+)/(?P<request_pk>\d+)/stornieren', 'transportation.views.cancel_or_reactivate_request', name="cancel_or_reactivate_request"),
    url(r'^anfrage/(?P<pk>\d+)/aendern/$', view= TransportationRequestUpdate.as_view(), name="update_request"),
    url(r'^anfrage/(?P<pk>\d+)/(?P<slug>[\w-]+)/(?P<request_pk>\d+)/$', 'transportation.views.transportation_request_view', name="transportation_request_view"),
    url(r'^$', 'transportation.views.transportation_startingpage', name='transportation_startingpage'),
    url(r'^biete_fahrt_an/$', 'transportation.views.register_transportation_offer', name="register_transportation"),
    url(r'^zwischenstopp_hinzufügen_zu/(?P<pk>\d+)/(?P<slug>[\w-]+)/$', 'transportation.views.add_additional_stops', name="add_additional_stops"),

    url(r'^zu_viele_passagiere/$', 'transportation.views.to_much_passengers', name="to_much_passengers"),
    url(r'^angebote/(?P<pk>\d+)/(?P<slug>[\w-]+)/$', 'transportation.views.details', name="transportation_details"),
    url(r'^suchen/(?P<pk>\d+)/(?P<slug>[\w-]+)/$', 'transportation.views.search_details', name="search_details"),
]