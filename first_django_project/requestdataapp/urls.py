from django.urls import path, re_path
from .views import *

app_name = "requestdataapp"
urlpatterns = [
    path("get/", process_get_view, name="get-view"),
    path("bio/", user_form, name="guser-form"),
    path("upload/", handle_file_upload, name="file-upload"),
]
