from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from markdown2 import Markdown
from random import choice
from . import util

def entry_exists(entry):
    entries = [file.lower() for file in util.list_entries()]
    return entry.lower() in entries

class new_page_form(forms.Form): 
    page_title = forms.CharField(widget = forms.TextInput(
        attrs = {
                "placeholder":"Page Title",
                "name": "page_title"
                }),
        label=''  
                )
    page_content = forms.CharField(widget = forms.Textarea(
        attrs = {
            "placeholder":"Page Content. Format using Markdown.",
            "name": "page_content",
            "cols": 35
            }),
        label=''
            )
    
class edit_page_form(forms.Form):
    page_content = forms.CharField(widget = forms.Textarea(
        attrs = {
            "name": "page_content",
            "cols": 35,
            'required': 'True'
            }),
        label='',
        required = False
            )

        

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def view_page(request, page_name):
    if (not util.get_entry(page_name)):
         return render(request, "encyclopedia/error.html", {
        "error_name": 'Page Not Found',
        "error_content": f"Error: Page '{page_name}' not found."
        })
    else:
        return render(request, "encyclopedia/entry.html", {
        "page_name": page_name,
        "page_content": Markdown().convert(util.get_entry(page_name))
        })

def add_page(request):
    if request.method == 'POST':
        if entry_exists(request.POST['page_title']):
            return render(request, "encyclopedia/error.html", {
            "error_name": 'Page already exists',
            "error_content": f"Error: Page '{request.POST['page_title']}' already exists."
            })
        else:
            util.save_entry(request.POST['page_title'], request.POST['page_content'])
            return view_page(request, request.POST['page_title'])

    return render(request, "encyclopedia/add.html", {
        "form": new_page_form()
    })

def random_page(request):
    r_page = choice(util.list_entries())
    return view_page(request, r_page)

def search_page(request): 
    if request.method == 'POST': 
        if entry_exists(request.POST['q']):
            return view_page(request, request.POST['q'])
        else:
            return results_page(request)

def results_page(request):
    entries_found = [entry for entry in util.list_entries() if request.POST['q'].lower() in entry.lower()]
    return render(request, "encyclopedia/results.html", {
        "entries": entries_found
    })

def edit_page(request, page_name):
    if request.method == "POST":
        form_data = edit_page_form(request.POST)
        if form_data.is_valid():
            util.save_entry(page_name, bytes(form_data.cleaned_data['page_content'], 'utf8'))
            return view_page(request, page_name)
    
    pre_content = util.get_entry(page_name)
    form = edit_page_form(initial = {'page_content': pre_content})
    return render(request, "encyclopedia/edit.html", {
        "editable_content": form,
        "page_name": page_name,
    })

    

