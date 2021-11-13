import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import markdown2


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def search_entries(searchstr):
    """
    Returns a list of all names of encyclopedia entries that contain
    the search parameter value. 
    """
    _, entries = list_entries()
    for entry in entries:
        if searchstr not in entry:
            entries.remove(entry)
    return entries


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8") 
    except FileNotFoundError:
        return None

def md2html(title):
    """
    Retrieves markdown from supplied title and converts to html.
    If no such title exists returns None.
    """
    md = get_entry(title) # retrieve markdown from entry file
    if md is None:
        return None
    else:
        return markdown2.markdown(md) # convert markdown text from file to html
