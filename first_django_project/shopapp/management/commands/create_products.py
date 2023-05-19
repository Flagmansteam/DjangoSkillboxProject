from django.core.management import BaseCommand


class Command(BaseCommand):
    """
    Create products
    """

    def handle(self, *args, **options):
        self.stdout.write("Create products")

        self.stdout.write(self.style.SUCCESS("Products created"))
