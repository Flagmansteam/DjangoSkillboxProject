from django.urls import path, re_path
from .views import *

app_name = "myapiapp"
urlpatterns = [
    path("hello/", hello_world_view, name="hello"),
    path("groups/", GroupsListView.as_view(), name="groups"),
]


