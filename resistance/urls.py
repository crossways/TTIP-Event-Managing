"""resistance URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

import spirit.urls

urlpatterns = [
    url(r'^', include('landingpage.urls', namespace='landingpage')),
    # url(r'^fahrten/', include('transportation.urls', namespace='transportation')),
    url(r'^uebernachtungen/', include('bednbreakfast.urls', namespace='bednbreakfast')),
    url(r'^special-events/', include('event.urls', namespace='event')),
    url(r'^mitglieder/', include('user.urls', namespace='user')),
    url(r'^comments/', include('django_comments.urls')),
    url(r'^forum/', include(spirit.urls), name='forum'),
    url(r'^admin/', include(admin.site.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)