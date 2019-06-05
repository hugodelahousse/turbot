from django.urls import path

from polls import views

app_name = "polls"
urlpatterns = [
    path("create", views.create, name="create"),
    path("create-unique", views.create_unique, name="create-unique"),
]
