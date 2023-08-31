from django.urls import path

from myapiapp import views

urlpatterns = [
    path('hello/', views.hello_world_view),
    path('groups/', views.GroupsListView.as_view()),
]
