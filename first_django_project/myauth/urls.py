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
    path("hello/", HelloView.as_view(), name="hello"),
    path("about-me/", AboutMeView.as_view(), name="about-me"),
    path("register/", RegisterView.as_view(), name="register"),
    path("users/", UserListView.as_view(), name="users_list"),
    path("users/<str:username>/", UserDetailView.as_view(), name="user_detail"),
    path("update_avatar/<int:pk>/", AvatarUpdateView.as_view(), name="update_avatar"),
    path("cookie/get", get_cookie_view, name="cookie-get"),
    path("cookie/set", set_cookie_view, name="cookie-set"),
    path("session/set", set_session_view, name="session-set"),
    path("session/get", get_session_view, name="session-get"),
    path("foo-bar", FooBarView.as_view(), name="foo-bar"),
]

