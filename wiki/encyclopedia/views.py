from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django import forms
from django.urls import reverse
import logging
from . import util
from .forms import AddEntryForm
from .forms import EditEntryForm
from .forms import SearchForm

log = logging.getLogger(__name__)

def index(request):
    if "entries" not in request.session:
        request.session["entries"] = []
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

def edit(request, title):
    request.session["title"] = title
    if request.method == "POST":
        # save the new markdown for the entry and present to the user as HTML
        log.info(f"User has submitted modified markdown for {title}.")
        form = EditEntryForm(request.POST)
        
        if form.is_valid():
            log.info("Edit entry form is valid.")
            # textarea bug, use bytes to avoid converting Windows CR LF to CR CR LF
            entryBody = bytes(form.cleaned_data["entryBody"],'utf8') 
            util.save_entry(title, entryBody)
            return HttpResponseRedirect(reverse('wiki:entry', args=(title,)))
        
        else:
            log.info("Edit entry form is invalid, so going back to fix it.")
            return render(request, "encyclopedia/edit.html", {
                "title": title, 
                "form": form
            })

    else :
        # load edit form with entry markdown and present to the user for editing
        log.info(f"User has opened { request.session['title'] } for editing.")
        form = EditEntryForm(data={'entryBody': util.get_entry(title)})
        return render(request, "encyclopedia/edit.html", {
            "title": title, 
            "form": form
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

def add(request):
    # process user input if user has added a new entry
    if request.method == "POST":
        log.info("Processing a new entry form.")
        form = AddEntryForm(request.POST)
        
        if form.is_valid():
            log.info("New entry form is valid.")
            title = form.cleaned_data["title"]
            entryBody = form.cleaned_data["entryBody"]
            util.save_entry(title, entryBody)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "entryBody": util.md2html(title)
            })

        else:
            # An entry already exists for this title or input is invalid so display an error message
            log.info("New entry form is not valid.")
            return render(request, "encyclopedia/add.html", {"form": form})
            
    # route if request method is GET (User has clicked the sidebar link).
    log.info("User has requested a blank add entry form.")
    return render(request, "encyclopedia/add.html", {"form": AddEntryForm()})

