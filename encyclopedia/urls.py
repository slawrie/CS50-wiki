from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.entry, name="entry_name"),
    path("search/", views.search, name="search_results"),
    path("add/", views.add, name="add"),
    path("edit/", views.edit, name="edit_entry"),
    path("random/", views.random, name="random")
    ]
