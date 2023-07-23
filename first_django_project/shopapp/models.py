from typing import Iterable
from django.contrib.auth.models import User
from django.db import models



def product_preview_directory_path(instance:"Product", filename: str)->str:
    return "products/product_{pk}/{filename}".format(
        pk=instance.pk,
        filename=filename,
    )


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
    created_by = models.ForeignKey(User, db_column="created_by", on_delete=models.CASCADE, null=True, default=None)
    archived = models.BooleanField(default=False)
    preview = models.ImageField(null=True, blank=True, upload_to=product_preview_directory_path)

    def __str__(self) -> Iterable[str]:
        return f"Product(pk={self.pk}, name={self.name!r})"

    # @property
    # def description_short(self)-> str:
    #     if len(self.description) < 48:
    #         return self.description
    #     return self.description[:48]+"..."
def product_images_directory_path(instance:"ProductImage", filename:str)-> str:
    return "products/product_{pk}/images/{filename}".format(
        pk=instance.product.pk,
        filename=filename,
    )

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=product_images_directory_path)
    description = models.CharField(max_length=200, null=False, blank=True)


class Order(models.Model):
    delivery_adress = models.TextField(null=True, blank=True)
    promocode = models.CharField(max_length=20, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    description = models.TextField(null=False, blank=True)
    products =models.ManyToManyField(Product, related_name="orders")  #Связь с заказом на продукте идёт через orders
# Поле receipt для загрузки чека после завершения заказа
    receipt = models.FileField(null=True, upload_to='orders/receipts/')
def __str__(self):
    return f"{self.delivery_adress}({self.user},{self.promocode}"