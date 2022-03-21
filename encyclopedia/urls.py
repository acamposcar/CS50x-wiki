from django.urls import path
from django.conf.urls import handler400, handler403, handler404

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new/", views.new, name="new"),
    path("random/", views.random_entry, name="random_entry"),
    path("search/", views.search, name="search"),
    path("wiki/<str:title>/", views.entry, name="entry"),
    path("wiki/<str:title>/edit/", views.edit, name="edit")
]
