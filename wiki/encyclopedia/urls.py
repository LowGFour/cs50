from django.urls import path
from . import views

# we want to map encyclopedia urls to 'wiki' instead of 'encyclopedia'
app_name= "wiki"

urlpatterns = [
    path("", views.index, name="index"),
    path("index/", views.index, name="index"),
    path("edit/<str:title>/", views.edit, name="edit"),
    path("randomEntry/", views.randomEntry, name="randomEntry"),
    path("search/", views.search, name="search"),
    path("add/", views.add, name="add"),
    path("<str:title>/", views.entry, name="entry")
]

# Note to self: the URL pattern choice for entry was mandated in the specifications.
# This particular pattern seems to be problematic for the reverse function. It was
# perhaps a deliberate design choice as it ensured a certain amount of research and
# experimentation was necessary for it to work in conjunction with other features.
# I think some of this "pain" could be avoided by using a more specific pattern, such
# as "read/<str:title>/" instead.