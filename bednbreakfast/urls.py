from django.conf.urls import include, url

urlpatterns = [
    url(r'^$', 'bednbreakfast.views.bednbreakfast_startingpage', name='bednbreakfast_startingpage'),
]