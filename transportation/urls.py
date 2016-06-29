from django.conf.urls import include, url

urlpatterns = [
    url(r'^$', 'transportation.views.transportation_startingpage', name='transportation_startingpage'),
]