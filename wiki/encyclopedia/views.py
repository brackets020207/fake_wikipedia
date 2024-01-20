from django.shortcuts import render
from django.http import HttpResponse

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def view_page(request, page_name):
    return render(request, "encyclopedia/entry.html", {
        "page_name": page_name,
        "page_content": util.get_entry(page_name)
    })

    

