from django.shortcuts import render
from . import util
import markdown2

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    md = util.get_entry(title) # retrieve markdown from entry file
    if md is None:
        html = f"<h1>Error</h1><p>No entry has been found for the supplied title: {title}</p>"
    else :
        html = markdown2.markdown(md) # convert markdown text from file to html
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entryBody": html
    })