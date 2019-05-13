from django.urls import path

from reddit import views

app_name = 'reddit'
urlpatterns = [
    path('subscribe', views.subscribe, name='subscribe'),
    path('unsubscribe', views.unsubscribe, name='unsubscribe'),
    path('trigger', views.trigger, name='trigger'),
]
