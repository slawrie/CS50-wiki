from django import forms

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title", initial='Entry title')
    content = forms.CharField(widget=forms.Textarea, label="Content", initial='# Title Heading')
