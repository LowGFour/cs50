from django.urls import path
from . import views

# we want to map encyclopedia urls to 'wiki' instead of 'encyclopedia'
app_name= "wiki"

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("<str:title>", views.entry, name="entry")
]
