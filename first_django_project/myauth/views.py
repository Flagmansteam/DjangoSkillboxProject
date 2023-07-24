from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import LogoutView
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView, ListView
from .models import Profile  # чтобы у новых пользователей появляля профиль
from .forms import *


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


class FooBarView(View):
    def get(self,request:HttpRequest)->JsonResponse:
        return JsonResponse({"foo":"bar", "spam":"eggs"})


def about_me(request: HttpRequest):
    user_profile = request.user.userprofile

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('about-me')
    else:
        form = UserProfileForm(instance=user_profile)
        return render(request, 'about-me.html',{'form':form})

def user_list(request): # получаем все профили и передаём в шаблон
    users = Profile.objects.select_related('user').all()
    return render(request, 'myauth/users_list.html', {'users':users})

# class UserListView(ListView):
#     model = Profile
#     template_name = 'users_list.html'
#     context_object_name = 'users'

def user_detail(request,username): # Получаем пользоватеоя и его профиль с помощью имени и передаем в шаблон
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile,user=user)
    return render(request, 'myauth/about-me.html', {'user':user, 'profile':profile})


def update_avatar(request,pk):
    user = get_object_or_404(User, pk = pk)
    if not request.user.is_staff and request.user != user:
        return HttpResponse("You do not have permission to perform this action.")

    if 'avatar' in request.FILES:
        avatar = request.FILES['avatar']
        if avatar.size>2*1024*1024:
            return HttpResponseBadRequest("Avatar size is too large")

        if not avatar.content_type.startswith("image/"):
            return HttpResponseBadRequest("Invalid file type. Only images are allowed")

        user.avatar = avatar
        return HttpResponse("Avatar updated successfully")

    else:
        return HttpResponseBadRequest("No avatar file was provided")

    return render(request, 'myauth/update_avatar.html',{'form':form, 'user':user})