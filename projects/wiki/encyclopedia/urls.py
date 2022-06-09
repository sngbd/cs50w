from django.urls import path

from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.wiki, name="wiki"),
    path("search/", views.search, name="search"),
    path("edit/<str:page>/", views.edit, name="edit"),
    path("edit/edited", views.edited, name="edited"),
    path("create/", views.create, name="create"),
    path("create/new/", views.new, name="new"),
    path("random/", views.random, name="random"),
]
