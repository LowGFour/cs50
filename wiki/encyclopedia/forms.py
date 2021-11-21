from django import forms
from django.core.exceptions import ValidationError
import logging
from . import util


log = logging.getLogger(__name__)

class SearchForm(forms.Form):
    q = forms.CharField()

class AddEntryForm(forms.Form):
    title=forms.CharField(label='Entry Title', max_length=20, required=True)
    entryBody=forms.CharField(label='Entry Markdown',max_length=2000, required=True, widget=forms.Textarea)
    
    # validator to check if an entry already exists for supplied title
    def clean_title(self):
        log.info("Checking to see if title has been used by a previous entry.")
        clnTitle = self.cleaned_data['title']
        if util.get_entry(clnTitle) is not None: 
            raise ValidationError(
                ("An entry called %(existingTitle)s already exists! Choose a new name for your entry."),
                params={'existingTitle': clnTitle}
            )
        return clnTitle
