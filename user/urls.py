from django.conf.urls import url, include

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', 'user.views.view_transportation_in_profile', kwargs={'slug': "", }, name='view_transportation_in_profile'),
    url(r'^(?P<pk>\d+)/(?P<slug>[\w-]+)/angebotene_fahrten/$', 'user.views.view_transportation_in_profile', name="view_transportation_in_profile"),
    url(r'^(?P<pk>\d+)/(?P<slug>[\w-]+)/angefragte_fahrten/$', 'user.views.view_transportation_requests_in_profile', name="view_transportation_requests_in_profile"),
    ]