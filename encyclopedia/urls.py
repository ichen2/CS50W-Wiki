from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.search, name="search"),
    path("new/", views.new, name="new"),
    path("error/", views.error, name="error"),
    path("random/", views.random, name="random"),
    path("<str:name>/", views.entry, name="entry"),
    path("<str:name>/edit/", views.edit, name="edit")
]
