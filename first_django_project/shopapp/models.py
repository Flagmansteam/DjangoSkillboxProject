from typing import Iterable
from django.contrib.auth.models import User
from django.db import models

class Product(models.Model):
    class Meta:
        ordering = ["name", "price"]
        # db_table = "tech_products"
        verbose_name_plural = "Products"

    name = models.CharField(max_length=100)
    description = models.TextField(null=False, blank=True)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    discount = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, db_column="created_by", on_delete=models.CASCADE,null=True, default=None)
    archived = models.BooleanField(default=False)

    def __str__(self) -> Iterable[str]:
        return f"Product(pk={self.pk}, name={self.name!r})"

    # @property
    # def description_short(self)-> str:
    #     if len(self.description) < 48:
    #         return self.description
    #     return self.description[:48]+"..."


class Order(models.Model):
    delivery_adress = models.TextField(null=True, blank=True)
    promocode = models.CharField(max_length=20, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    products =models.ManyToManyField(Product, related_name="orders")  #Связь с заказом на продукте идёт через orders

def __str__(self):
    return f"{self.delivery_adress}({self.user},{self.promocode}"