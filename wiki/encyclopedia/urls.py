from django.urls import path
from . import views

# we want to map encyclopedia urls to 'wiki' instead of 'encyclopedia'
app_name= "wiki"

urlpatterns = [
    path("", views.index, name="index"),
    path("index/", views.index, name="index"),
    path("edit/<str:title>/", views.edit, name="edit"),
    path("search/", views.search, name="search"),
    path("add/", views.add, name="add"),
    path("<str:title>/", views.entry, name="entry")
]
