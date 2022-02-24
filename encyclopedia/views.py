from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms

from . import util
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
            "entry": entry
        })
    else:
        return render(request, "encyclopedia/404.html")

# TODO        
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

# TODO: redirect to entry url (use reverse)
def random_entry(request):
    title = random.choice(util.list_entries())
    entry = util.get_entry(title)
    return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": entry
        })

# TODO  
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