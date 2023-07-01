from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # если User будет удален, то нужно удалять и Profile
    bio=models.TextField(max_length=500, blank=True)
    argeement_accepted=models.BooleanField(default=False)

