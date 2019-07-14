from functools import partial

from django.urls import path

from polls import views

app_name = "polls"
urlpatterns = [
    path("create", views.create, name="create"),
    path("create-unique", partial(views.create, unique=True), name="create-unique"),
    path(
        "create-anonymous",
        partial(views.create, anonymous=True),
        name="create-anonymous",
    ),
    path(
        "create-unique-anonymous",
        partial(views.create, unique=True, anonymous=True),
        name="create-unique-anonymous",
    ),
]
