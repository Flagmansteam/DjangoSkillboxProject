from typing import Sequence
from django.contrib.auth.models import User
from django.core.management import BaseCommand
from shopapp.models import  Product


# Позволяет вставлять несколько объектов за один запрос к базе данных
class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write("Start demo bulk actions")

        result = Product.objects.filter(
            name__contains="Smartphone"
        ).update(discount=10)  #всем товарам с определенным именем устанавливается значение дискаунта равное 10

        print(result)


        # info = [
        #     ('Smartphone 1', 199),
        #     ('Smartphone 2', 299),
        #     ('Smartphone 3', 399),
        # ]
        # products = [
        #     Product(name=name, price=price)
        #     for name, price in info
        # ]
        # print(products)
        #
        # result = Product.objects.bulk_create(products)
        # for obj in result:
        #     print(obj)
        #

        self.stdout.write("Done")
