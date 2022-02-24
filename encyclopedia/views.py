from django.shortcuts import render

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
        return render(request, "encyclopedia/index.html")
    else:
        return render(request, "encyclopedia/new.html")


# TODO: redirect to entry url (use reverse)
def random_entry(request):
    title = random.choice(util.list_entries())
    entry = util.get_entry(title)
    return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": entry
        })
        
# TODO  
def edit(request):
    pass