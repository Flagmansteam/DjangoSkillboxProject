from django.urls import path, re_path
from .views import *
from django.contrib.auth.views import LoginView, LogoutView

app_name = "myauth"
urlpatterns = [
    path(
        "login/",
        LoginView.as_view(
            template_name="myauth/login.html",
            redirect_authenticated_user=True
        ),
        name="login"),
    path("logout/", MyLogoutView.as_view(), name="logout"),
    path("about-me/", AboutMeView.as_view(), name="about-me"),
    path("register/", RegisterView.as_view(), name="register"),
    path("users/", user_list, name="user_list"),
    path("users/<str:username>/", user_detail, name="user_detail"),
    path("cookie/get", get_cookie_view, name="cookie-get"),
    path("cookie/set", set_cookie_view, name="cookie-set"),
    path("session/set", set_session_view, name="session-set"),
    path("session/get", get_session_view, name="session-get"),
    path("foo-bar", FooBarView.as_view(), name="foo-bar"),
]

