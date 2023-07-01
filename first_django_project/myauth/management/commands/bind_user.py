
from django.contrib.auth.models import  User, Group, Permission
from django.core.management import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        user= User.objects.get(pk=2)
        group,created = Group.objects.get_or_create(
            name="profile_manager"
        )
        permission_profile= Permission.objects.get(
            codename="view_profile",
        )
        permission_logentry = Permission.objects.get(
            codename="view_logentry",
        )

        group.permissions.add(permission_profile) #связать permission с группой
        user.groups.add(group) #связать user с группой
        user.user_permissions.add(permission_logentry)# связать user с permission

        group.save()
        user.save()
