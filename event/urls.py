from django.conf.urls import include, url

urlpatterns = [
    url(r'^$', 'event.views.event_startingpage', name='event_startingpage'),
]