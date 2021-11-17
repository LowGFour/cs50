from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django import forms
from django.urls import reverse
from . import util

class SearchForm(forms.Form):
    q = forms.CharField()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries() 
    })

def entry(request, title):
    html = util.md2html(title) 
    if html is None:
        html = f"<h1>Error</h1><p>No entry has been found for the supplied title: {title}</p>"
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entryBody": html
    })

def search(request):
    q = None # init q for function scope
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            # retrieve the search string from the form
            q = form.cleaned_data['q']

        if q is not None:
            # check for an entry matching the search string
            html = util.md2html(q)
            if html is None:
                # no perfect match so find any matching entries, go home
                # request.session["entries"] = util.search_entries(q)
                return render(request, "encyclopedia/index.html", {
                    "entries": util.search_entries(q)
                })
            else:
                # perfect match so display entry
                return render(request, "encyclopedia/entry.html", {
                    "title": q,
                    "entryBody": html
                })
        else:
            # q is none; form was submitted without a value, inadvertent submit, just go home
            return render(request, "encyclopedia/index.html", {})

# test change
