from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

import markdown2

from . import util
import os
from random import randrange


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def error(request):
    return render(request, "encyclopedia/error.html", {
        "name":request.session['error'][0]
    })

    
def entry(request,name):
    if request.method != 'POST':
        entry = util.get_entry(name)
        if(entry == None) :
            request.session['error'] = ["No entry exists for " + name]
            return HttpResponseRedirect(reverse("error"))
        else :
            return render(request, "encyclopedia/entry.html", {
                "name":name,
                "entry": markdown2.markdown(entry)
            })
    else :
        if "n" in request.POST:
            name = request.POST["n"]
            if(util.get_entry(name)!=None) :
                request.session['error'] = ["An entry for " + name + " already exists."]
                return HttpResponseRedirect(reverse("error"))
            else :
                description = request.POST["d"]
                util.save_entry(name,description)
                return render(request, "encyclopedia/entry.html", {
                    "name":name,
                    "entry": markdown2.markdown(util.get_entry(name))
                })
        elif "d" in request.POST:
            description = os.linesep.join([s for s in request.POST["d"].splitlines() if s])
            util.save_entry(name,request.POST["d"].strip())
            return render(request, "encyclopedia/entry.html", {
                "name":name,
                "entry": markdown2.markdown(description)
            })

def search(request):
    name = request.POST['q']
    entry = util.get_entry(name)
    results = []   
    if(entry == None) :

        for e in util.list_entries() :
            if name in e :
                results.append(e)

        return render(request, "encyclopedia/search_results.html", {
            "name":name,
            "results":results
        })
    else :
        return render(request, "encyclopedia/entry.html", {
            "name":name,
            "entry": markdown2.markdown(entry)
        })

def new(request):
    return render(request, "encyclopedia/new_page.html")

def edit(request,name):
    return render(request, "encyclopedia/edit.html", {
        "name":name,
        "entry":util.get_entry(name)
    })

def random(request):
    entries = util.list_entries()
    r = randrange(len(entries)-1)
    for entry in entries :
        if entries[r] == entry :
            return render(request, "encyclopedia/entry.html", {
                "name":entries[r],
                "entry": markdown2.markdown(util.get_entry(entries[r]))
            })


