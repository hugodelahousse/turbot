from django.urls import path

from polls import views

app_name = 'polls'
urlpatterns = [
    path('create', views.create, name='create'),
]
