from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms

from . import util
from markdown2 import Markdown


import random


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
        title = request.POST['title'].strip()
        content = request.POST['content']
        for existing_title in util.list_entries():
            if title.upper() == existing_title.upper().strip():
                return render(request, "encyclopedia/new.html", {
                    "title": title,
                    "content": content,
                    "message": "This entry already exists. Choose another title."
            })

        content = f"# {title} \n\n {content}"
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse("entry", kwargs={'title': title}))

    else:
        return render(request, "encyclopedia/new.html", {
            "title": "",
            "content": "",
            "message": ""
        })


def random_entry(request):
    title = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse("entry", kwargs={'title': title}))


 
def edit(request, title):
    if request.method == "POST":
        content = request.POST['content']
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse("entry", kwargs={'title': title}))

    else:
        entry = util.get_entry(title)
        if entry:
            return render(request, "encyclopedia/edit.html", {
                "title": title,
                "entry": entry
            })
        else:
            return render(request, "encyclopedia/404.html")

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