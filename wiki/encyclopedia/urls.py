from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("add", views.add_page, name = "add"),
    path("random", views.random_page, name = "random"),
    path("search", views.search_page, name = "search"),
    path("edit/<str:page_name>", views.edit_page, name = "edit"),
    path("<str:page_name>", views.view_page, name = "entry")
    
    
]
