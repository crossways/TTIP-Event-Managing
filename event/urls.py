from django.conf.urls import include, url

from .views import EventUpdate

urlpatterns = [
    url(r'^$', 'event.views.event_startingpage', name='event_startingpage'),
    url(r'^erstelle_event/$', 'event.views.register_event', name="register_event"),
    url(r'^(?P<pk>\d+)/(?P<slug>[\w-]+)/$', 'event.views.event_details', name="event_details"),
    url(r'^(?P<pk>\d+)/(?P<slug>[\w-]+)/aendern/$', view= EventUpdate.as_view(), name="change_event"),
    url(r'^event_stornieren_oder_einstellen/(?P<pk>\d+)/(?P<slug>[\w-]+)$', 'event.views.cancel_event_or_activate_again', name="cancel_or_activate"),

    url(r'^gesuch/(?P<pk>\d+)/(?P<slug>[\w-]+)/gesuch_einstellen/$', 'event.views.register_supportneeded', name="register_supportneeded"),

    url(r'^like/', include('event.like.urls', namespace='like')),
]