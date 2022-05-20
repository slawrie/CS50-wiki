from django.http import HttpResponse
from django.shortcuts import render
import markdown2
from . import util
from random import choice
from django.urls import reverse
from django.http import HttpResponseRedirect
from . import forms


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry_name = util.get_entry(title)
    entries = [ele.lower() for ele in util.list_entries()]
    if entry_name is None:
        return render(request, "encyclopedia/error.html", {
            "title": title,
            "entries": entries
        })
    else:
        content = markdown2.markdown(util.get_entry(title))
        return render(request, "encyclopedia/entry.html", {
        "content": content,
        "title": title,
        })

def search(request):
    query = request.GET.get('q').lower()
    entries = [ele.lower() for ele in util.list_entries()]
    if query in entries:
        return entry(request, title=query)
    else:
        results = [ele for ele in entries if query in ele]
        return render(request, "encyclopedia/search.html", {
            "entries": results
        })


def add(request):
    # Check if method is POST
    if request.method == "POST":

        # Take in the data the user submitted and save it as form
        form = forms.NewEntryForm(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():
            # Isolate the title and content from the 'cleaned' version of form data
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            # Add the new entry to our encyclopedia if it is not already there
            entries = [ele.lower() for ele in util.list_entries()]
            if title.lower() not in entries:
                util.save_entry(title, content)
                # Redirect user to new entry
                return entry(request, title=title)
            else:
                return render(request, "encyclopedia/error.html", {
                        "title": title.lower(),
                        "entries": entries
                        })
        else:
            # If the form is invalid, re-render the page with existing information.
            return render(request, "encyclopedia/add.html", {
                "form": form
            })

    return render(request, "encyclopedia/add.html", {
        "form": forms.NewEntryForm()
    })


def edit(request):
    # Displays form with prepopulated values if entry exists

    # Check if method is GET
    if request.method == "GET":
        title = request.GET.get('q').lower()
        content = markdown2.markdown(util.get_entry(title))
        # Prepopulate form and display it
        formEdit = forms.NewEntryForm(initial={'title': title.capitalize(), 'content': content})

        return render(request, "encyclopedia/edit.html", {
            "form": formEdit
        })

    else: #if POST
        # Take in the data the user submitted and save it as form
        form = forms.NewEntryForm(request.POST)
        # Check if form data is valid (server-side)
        if form.is_valid():
            # Isolate the title and content from the 'cleaned' version of form data
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            # Add the new entry to our encyclopedia if it is not already there
            entries = [ele.lower() for ele in util.list_entries()]
            util.save_entry(title, content)
            # Redirect user to new entry
            return entry(request, title=title)

        else:
            # If the form is invalid, re-render the page with existing information.
            return render(request, "encyclopedia/edit.html", {
                "form": form
            })


def random(request):
    # Get all entries, select and display a random one
    entries = util.list_entries()
    title = choice(entries)
    content = markdown2.markdown(util.get_entry(title))
    return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": content})