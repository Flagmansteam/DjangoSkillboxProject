from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.db import transaction
from shopapp.models import Order, Product

# загружаем необходимые данные из базы данных разными способами
class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Create order with products")
        user = User.objects.get(username="admin")
        # products: Sequence[Product] = Product.objects.defer("description", "price", "created_at").all()
        products: Sequence[Product] = Product.objects.only("id").all()
        order, created = Order.objects.get_or_create(
            delivery_adress="Ul.Popova, d.5",
            promocode="Promo5",
            user=user,
        )
        for product in products:
            order.products.add(product) # добавляем товары к заказу
        order.save()

        self.stdout.write(f"Created order {order}")



