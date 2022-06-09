from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect


from . import util
from random import choice
from markdown2 import Markdown


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def wiki(request, entry):
    title = None
    for i in util.list_entries():
        if entry.casefold() == i.casefold():
            title = i
            break
    if title is None:
        return render(request, "encyclopedia/error.html", {
            "title": "Error: 404 Not Found",
            "message_title": "404 Not Found",
            "message": f"{entry} was not found."
        })
    page = util.get_entry(title)
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": Markdown().convert(page)
    })
    

def search(request):
    result = request.GET['q']
    list = []
    for x in util.list_entries():
        if result.casefold() == x.casefold():
            list.append(x)
            break
    if list:
        return HttpResponseRedirect(reverse("wiki:wiki", kwargs={'entry': list[0]}))
    else:
        list2 = []
        for i in util.list_entries():
            if result.casefold() in i.casefold():
                list2.append(i)
        return render(request, "encyclopedia/search.html", {
            "term": result,
            "results": list2
        })


def create(request):
    return render(request, "encyclopedia/create.html")


def new(request):
    title = request.GET['title']
    content = request.GET['content']
    if title == "":
        return render(request, "encyclopedia/error.html", {
            "title": "Error: 400 Bad Request",
            "message_title": "400 Bad Request",
            "message": "Title is empty."
        })
    for i in util.list_entries():
        if title.casefold() in i.casefold():
            return render(request, "encyclopedia/error.html", {
                "title": "Error: 409 Conflict",
                "message_title": "409 Conflict",
                "message": "Title already exists."
            })
    util.save_entry(title, content)
    return HttpResponseRedirect(reverse("wiki:wiki", kwargs={'entry': title}))


def edit(request, page):
    entry = util.get_entry(page)
    if entry is None:
        return render(request, "encyclopedia/error.html", {
            "title": "Error: 404 Not Found",
            "message_title": "404 Not Found",
            "message": f"{page} was not found."
        })
    return render(request, "encyclopedia/edit.html", {
        "page": page,
        "entry": entry
    })


def edited(request):
    title = request.GET['title']
    content = request.GET['content']
    if title == "":
        return render(request, "encyclopedia/error.html", {
            "title": "Error: 400 Bad Request",
            "message_title": "400 Bad Request",
            "message": "Title is empty"
        })
    util.save_entry(title, content)
    return HttpResponseRedirect(reverse("wiki:wiki", kwargs={'entry': title}))


def random(request):
    pick = choice(util.list_entries())
    return HttpResponseRedirect(reverse("wiki:wiki", kwargs={'entry': pick}))
