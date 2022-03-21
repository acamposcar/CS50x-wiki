from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms

from . import util
from markdown2 import Markdown

import random


class NewEntry(forms.Form):
    title = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "Title", "class": "form-control"}),  required=True)
    content = forms.CharField(widget=forms.Textarea(
        attrs={"placeholder": "Content (using Markdown syntax)", "rows": 15, "class": "form-control"}), required=True)


class EditEntry(forms.Form):
    content = forms.CharField(widget=forms.Textarea(
        attrs={"rows": 15, "class": "form-control"}), required=True)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    entry = util.get_entry(title)
    if entry:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": Markdown().convert(entry)
        })
    else:
        return render(request, "encyclopedia/404.html")


def new(request):
    if request.method == "POST":
        form = NewEntry(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"].strip()
            content = form.cleaned_data["content"]
            for existing_title in util.list_entries():
                if title.upper() == existing_title.upper().strip():
                    return render(request, "encyclopedia/new.html", {
                        "form": form,
                        "message": "This entry already exists. Choose another title."
                    })
        else:
            return render(request, "encyclopedia/new.html", {
                "form": form,
                "message": ""
            })
        content = f"# {title} \n\n {content}"
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse("entry", kwargs={'title': title}))

    else:
        return render(request, "encyclopedia/new.html", {
            "form": NewEntry(),
            "message": ""
        })


def random_entry(request):
    title = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse("entry", kwargs={'title': title}))


def edit(request, title):
    if request.method == "POST":
        form = EditEntry(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("entry", kwargs={'title': title}))
        else:
            return render(request, "encyclopedia/edit.html", {
                "title": title,
                "form": form
            })
    else:
        entry = util.get_entry(title)
        if entry:
            return render(request, "encyclopedia/edit.html", {
                "title": title,
                "form": EditEntry(initial={'title': title, 'content': entry})
            })


def search(request):
    text = request.GET['q'].strip()
    entry = util.get_entry(text)
    entries = util.list_entries()
    search_result = []

    for existing_title in entries:
        if text.upper() == existing_title.upper().strip():
            return HttpResponseRedirect(reverse("entry", kwargs={'title': existing_title}))

    for existing_title in entries:
        if text.upper() in existing_title.upper().strip():
            search_result.append(existing_title)
    if search_result:
        return render(request, "encyclopedia/search.html", {
            "entries": search_result,
            "message": ""
        })
    else:
        return render(request, "encyclopedia/search.html", {
            "entries": "",
            "message": "Article not found"
        })


def bad_request(request, exception):
    context = {}
    return render(request, 'error.html', {
        "title": "Error 400",
        "message": "Bad request"
    }, context, status=400)


def permission_denied(request, exception):
    context = {}
    return render(request, 'error.html', {
        "title": "Error 403",
        "message": "Forbidden"
    }, context, status=403)


def page_not_found(request, exception):
    context = {}
    return render(request, 'error.html', {
        "title": "Error 404",
        "message": "Page not found"
    }, context, status=404)
