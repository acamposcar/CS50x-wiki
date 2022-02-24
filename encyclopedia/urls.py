from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new/", views.new, name="new"),
    path("random/", views.random_entry, name="random_entry"),
    path("<str:title>/", views.entry, name="entry"),
    path("<str:title>/edit/", views.edit, name="edit")

]
