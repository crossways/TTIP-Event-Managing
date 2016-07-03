from django.conf.urls import url, include

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', 'resistance.user.views.view_user_recipes_in_profile', kwargs={'slug': "", }, name='view_user_recipes_in_profile'),
    url(r'^(?P<pk>\d+)/(?P<slug>\w+)/$', 'resistance.user.views.view_user_recipes_in_profile', name="view_user_recipes_in_profile")
    ]