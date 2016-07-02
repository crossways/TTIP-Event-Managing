from django.conf.urls import include, url

urlpatterns = [
    url(r'^(?P<pk>\d+)/(?P<slug>[\w-]+)/$', 'transportation.views.details', name="details"),
    url(r'^$', 'transportation.views.transportation_startingpage', name='transportation_startingpage'),
    url(r'^biete_fahrt_an/$', 'transportation.views.register_transportation_offer', name="register_transportation"),
]