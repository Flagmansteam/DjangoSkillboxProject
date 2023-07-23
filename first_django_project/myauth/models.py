from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.shortcuts import get_object_or_404, render


# Create your models here.
def custom_upload_to(instance, filename):
    return 'avatars/{}/{}'.format(instance.user.username,filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # если User будет удален, то нужно удалять и Profile
    bio = models.TextField(max_length=500, blank=True)
    argeement_accepted = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to=custom_upload_to, null=True, blank=True)

def user_detail(request, user_id):
    user= get_object_or_404(User, id=user.id)
    return render(request, 'user_detail.html', {'user':user})

