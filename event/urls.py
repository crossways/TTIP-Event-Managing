from django.conf.urls import include, url

from .views import EventUpdate, SupportNeededUpdate

urlpatterns = [
    url(r'^$', 'event.views.event_startingpage', name='event_startingpage'),
    url(r'^erstelle_event/$', 'event.views.register_event', name="register_event"),
    url(r'^(?P<pk>\d+)/(?P<slug>[\w-]+)/$', 'event.views.event_details', name="event_details"),
    url(r'^(?P<pk>\d+)/(?P<slug>[\w-]+)/aendern/$', view=EventUpdate.as_view(), name="change_event"),
    url(r'^event_stornieren_oder_einstellen/(?P<pk>\d+)/(?P<slug>[\w-]+)$', 'event.views.cancel_event_or_activate_again', name="cancel_or_activate"),

    url(r'^gesuch/(?P<pk>\d+)/(?P<slug>[\w-]+)/gesuch_einstellen/$', 'event.views.register_supportneeded', name="register_supportneeded"),
    url(r'^gesuch/(?P<pk>\d+)/(?P<slug>[\w-]+)/(?P<support_pk>\d+)/(?P<support_slug>[\w-]+)/$',
        'event.views.supportneeded_details',
        name="supportneeded_details"
        ),
    url(r'^gesuch/(?P<pk>\d+)/(?P<support_slug>[\w-]+)/aendern/$',
        view=SupportNeededUpdate.as_view(),
        name="change_supportneeded"),
    url(r'^gesuch/(?P<pk>\d+)/(?P<slug>[\w-]+)/(?P<support_pk>\d+)/(?P<support_slug>[\w-]+)/stornieren$',
        'event.views.cancel_supportneeded_or_activate_again',
        name="cancel_supportneeded_or_activate_again"
        ),
    url(r'^gesuch/(?P<pk>\d+)/(?P<slug>[\w-]+)/(?P<support_pk>\d+)/(?P<support_slug>[\w-]+)/unterstuetzung_anbieten/$',
        'event.views.register_supportoffer',
        name="register_supportoffer"
        ),
    url(r'^gesuch/(?P<pk>\d+)/(?P<slug>[\w-]+)/(?P<support_pk>\d+)/(?P<support_slug>[\w-]+)/unterstuetzung/(?P<offer_pk>\d+)/$',
        'event.views.supportoffer_details',
        name="supportoffer_details"
        ),
    url(
        r'^gesuch/(?P<pk>\d+)/(?P<slug>[\w-]+)/(?P<support_pk>\d+)/(?P<support_slug>[\w-]+)/unterstuetzung/(?P<offer_pk>\d+)/stornieren$',
        'event.views.cancel_or_reactivate_supportoffer',
        name="cancel_or_reactivate_supportoffer"
        ),

    url(r'^suchen/$', 'event.views.search_event', name="search_event"),
    url(r'^suchen/ergebnisse/$', 'event.views.view_search_results', name="view_search_results"),

    url(r'^like/', include('event.like.urls', namespace='like')),
]

