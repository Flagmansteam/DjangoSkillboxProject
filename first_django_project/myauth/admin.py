from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile
from .forms import UserProfileForm

class UserProfileInline(admin.StackedInline):
        model = Profile
        can_delete = False

class UserAdmin(UserAdmin):
        inlines = (UserProfileInline, )
        form = UserProfileForm

admin.site.unregister(User)
admin.site.register(User, UserAdmin)