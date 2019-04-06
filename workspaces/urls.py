from django.urls import path

from workspaces import views

urlpatterns = [
    path('oauth', views.oauth, name='oauth'),
    path('action', views.action, name='action'),
    path('test', views.test, name='test'),
]

