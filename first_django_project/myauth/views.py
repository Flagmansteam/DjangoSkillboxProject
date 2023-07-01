from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import LogoutView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, CreateView
from .models import  Profile #  чтобы у новых пользователей появляля профиль

class AboutMeView(TemplateView):
    template_name ="myauth/about-me.html"

class RegisterView(PermissionRequiredMixin, CreateView):
    form_class = UserCreationForm
    template_name = "myauth/register.html"
    permission_required = "shopapp:add_product"
    success_url = reverse_lazy("myauth:about-me")

    def form_valid(self, form):
        response = super().form_valid(form) # здесь происходит регистрация нового пользователя
        Profile.objects.create(user=self.object)# здесь происходит создание профиля нового пользователя
        username = form.cleaned_data.get("username")# здесь происходит аутентификация нового пользователя
        password = form.cleaned_data.get("password1")
        user = authenticate(
            self.request,
            username=username,
            password=password,

        )
        login(request=self.request, user=user)

        return response

def login_view(request:HttpRequest):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/admin/')

        return render(request, 'myauth/login.html')

    username = request.POST["username"]
    # чтобы выполнить аутентификацию пользователя переопределили стандартное поеведение. Cразу после регистрации пользователь попадает в систему
    password = request.POST["password"]

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request,user)
        return redirect("/admin")


    return render(request, "myauth/login.html", {"error": "Invalid login credentials"})

def logout_view(request:HttpRequest):
    logout(request)
    return redirect(reverse("myauth:login"))

class MyLogoutView(LogoutView):
    next_page = reverse_lazy("myauth:login")

@user_passes_test(lambda u: u.is_superuser)
def set_cookie_view(request:HttpRequest)->HttpResponse:
    response=HttpResponse("Cookie set")
    response.set_cookie("fizz", "buzz", max_age=3600)
    return response

def get_cookie_view(request:HttpRequest)->HttpResponse:
    value = request.COOKIES.get("fizz","default value")
    return HttpResponse(f"Cookie value: {value!r}")

@permission_required("myauth:view_profile", raise_exception=True)
def set_session_view(request:HttpRequest)->HttpResponse:
    request.session["foobar"]= "spameggs"
    return HttpResponse("Session set!")

@login_required # проверка юзера на ауттентификацию
def get_session_view(request:HttpRequest)->HttpResponse:
    value = request.session.get("foobar", "default")
    return HttpResponse(f"Session value: {value!r}")


