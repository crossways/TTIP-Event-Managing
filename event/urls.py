from django.conf.urls import include, url

urlpatterns = [
    url(r'^$', 'event.views.event_startingpage', name='event_startingpage'),
    url(r'^like/', include('event.like.urls', namespace='like')),
]