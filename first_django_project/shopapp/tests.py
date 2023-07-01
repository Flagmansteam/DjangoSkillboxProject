from django.test import TestCase
from django.urls import reverse
from string import ascii_letters
from random import choices

from .models import Product
from .utils import add_two_numbers


class AddTwoNumbersTestCase(TestCase):
    def test_add_two_numbers(self):
        result = add_two_numbers(2,3)
        self.assertEqual(result,5)


class ProductCreateViewTestCase(TestCase):
    def setUp(self)->None:  # для предварительной настройки
        self.product_name ="".join(choices(ascii_letters, k=10)) # получение рандомного имени продукта
        Product.objects.filter(name=self.product_name).delete() # проверка и удаленеи объектов в случаем одинаковых названий
    def test_create_product(self):
        response = self.client.post(reverse("shopapp:product_create"), {
            "name": self.product_name,
            "price": "123.45",
            "description": "Good Table",
            "discount": "10"
        }
        )
        self.assertRedirects(response, reverse("shopapp:products_list"))
        self.assertTrue(Product.objects.filter(name=self.product_name).exists()) # проверка, что продукт создан

class ProductDetailsViewTestCase(TestCase):
   @classmethod
   def setUpClass(cls):
        cls.product = Product.objects.create(name="Best Product")

    # def setUp(self)->None:
    #     self.product = Product.objects.create(name="Best Product")

   @classmethod
   def tearDownClass(cls):
       cls.product.delete()

   def test_get_product_nd_check_content(self): # проверить статус кода и содержимое ответа на наличие имени продукта. Для всех тестов сущность создана один раз перед выполнением.
       response = self.client.get(
           reverse("shopapp:product_details", kwargs={"pk": self.product.pk})
       )
       self.assertContains(response, self.product.name)

   # def tearDown(self)->None: # после выполнения удаляется выбранный продукт,выполняется после каждого теста вне зависимости от успешности выполнения
   # self.product.delete() agent
