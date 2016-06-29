from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static


import spirit.urls

urlpatterns = [
    url(r'^$', 'landingpage.views.landingpage_view', name='landingpage'),
]


