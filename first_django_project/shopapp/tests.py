from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from string import ascii_letters
from random import choices
from django.conf import settings
from .models import Product, Order
from .utils import add_two_numbers


class AddTwoNumbersTestCase(TestCase):
    def test_add_two_numbers(self):
        result = add_two_numbers(2,3)
        self.assertEqual(result,5)


class ProductCreateViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='bob_test', password='qwerty')
        permission = Permission.objects.get(codename='add_product')
        cls.user.user_permissions.add(permission)
        print('User has perm1:', cls.user.has_perm('add_product'))

    def setUp(self) -> None:  # для предварительной настройки
        self.user = User.objects.get(username='bob_test')
        self.client.force_login(self.user)
        print('User has perm2:', self.user.has_perm('add_product'))
        self.product_name = "".join(choices(ascii_letters, k=10))  # получение рандомного имени продукта
        Product.objects.filter(
            name=self.product_name).delete()  # проверка и удаленеи объектов в случаем одинаковых названий


    @classmethod
    def tearDownClass(cls):  # Удаление пользователя
        super().tearDownClass()
        User.objects.filter(username='bob_test').delete()


    def test_create_product(self):
        response = self.client.post(
            reverse("shopapp:product_create"),
            {
            "name": self.product_name,
            "price": "123.45",
            "description": "Good Table",
            "discount": "10",
            }
        )
        self.assertRedirects(response, reverse("shopapp:products_list"))
        self.assertTrue(
            Product.objects.filter(name=self.product_name).exists()
        ) # проверка, что продукт создан




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

# создаём тест, который будет проверять получение списка продуктов

class ProductListViewTestCase(TestCase):
    fixture = [
        'products-fixture.json',
    ] # можно передавать отдельно по заказам, продуктам и т.д.

    def test_products(self):
        response = self.client.get(reverse("shopapp:products_list"))
        # products = Product.objects.filter(archived=False).all()  взято из базы
        # products_ = response.context["products"]    находятся в контексте
        # for p,p_ in zip(products, products_):
        #     self.assertEqual(p.pk, p_.pk)
        self.assertQuerysetEqual(
            qs = Product.objects.filter(archived=False).all(), # данные,которые ожидаем получить
            values=(p.pk for p in response.context["products"]), # данные, которые получили
            transform=lambda p:p.pk,
        )
        self.assertTemplateUsed(response, 'shopapp/products-list.html')


class OrdersListViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        # cls.credentials = dict(username="bob_test", password="qwerty")
        # cls.user = User.objects.create_user(**cls.credentials)
        cls.user = User.objects.create_user(username="bob_test", password ="qwerty")

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self)->None:  #аутентификация пользователя
        # self.client.login(**self.credentials)
        self.client.force_login(self.user)
    def test_orders_view(self):
        response = self.client.get(reverse("shopapp:order_list"))
        self.assertContains(response, "Orders")

# добавим тест, чтобы проверить анонимного пользователя, сделать выход пользователя.  Убедимся, что если пользователь не выполнил вход, то при попытке  запросить список заказов пользователь будет перенаправлен на страницу для входа в приложение


    def test_orders_view_not_authenticated(self):
        self.client.logout()# выполняемтся выход пользователя, вход которого произведен этапом ранее
        response = self.client.get(reverse("shopapp:order_list"))
        # self.assertRedirects(response, str(settings.LOGIN_URL))
        self.assertEqual(response.status_code, 302)
        self.assertIn(str("/accounts/login/"), response.url)

# создание апи для выгрузки инфо по продуктам

# python manage.py test shopapp.tests.ProductsExportViewTestCase
class ProductsExportViewTestCase(TestCase):
    fixtures = ['products-fixtures.json']

    def test_get_products_view(self): # тест, который проверяет, что данные которые выгрузили совпадают с базой
        response = self.client.get(reverse("shopapp:products-export"))
        self.assertEqual(response.status_code,200)
        products = Product.objects.order_by("pk").all()
        expected_data = [
            {
                "pk": product.pk,
                "name": product.name,
                "price": str(product.price),
                "archived": product.archived,
            }
            for product in products
        ]
        products_data = response.json(),
        self.assertEqual(products_data['products'], expected_data)


class OrderDetailViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user = User.objects.create_user(username="bob_test", password="qwerty")
        permission = Permission.objects.get(codename ='view_order')
        user.user_permissions.add(permission)


    def setUp(self):
       self.client.force_login(self.user)
       self.order =Order.objects.create(name ='Test Order', promocode = '10',delivery_adress = 'The best city')

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass(cls)
        User.objects.filter(username="bob_test").delete()
    def tearDown(self):
        self.order.delete()

    def test_order_details_view(self):
        url = reverse("shopapp:order_details", kwargs = {'pk': self.order.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,str(self.order.promocode))
        self.assertContains(response, str(self.order.delivery_adress))
        self.assertTemplateUsed((response, 'order_detail.html'))



class OrdersExportTestCase(TestCase):
    fixtures = [
        'users.json',
        'products.json',
        'orders.json',
    ]
    @classmethod
    def setUpClass(cls): # Создание пользвателя и добавление разрешения на просмотр заказов
        super().setUpClass()
        user = User.objects.create_user(username='testuser', password='testpassword')
        permission = Permission.objects.get(codename='view_order')
        user.user_permissions.add(permission)

    def setUp(self):
        self.client.force_login(self.user)

    @classmethod
    def tearDownClass(cls): # Удаление пользователя
        super().tearDownClass()
        User.objects.filter(username='testuser').delete()

    def test_orders_export(self):
        self.load_fixture('users.json') # Загружаем фикстуры
        self.load_fixture('products.json')
        self.load_fixture('orders.json')

        response = self.client.get(reverse("shopapp:orders-export")) # Отправляем запрос на выгрузку заказов
        self.assertEqual(response.status_code, 200)

        expected_data = [
            {
                'order_id': 1,
                'address': 'Pupkin street',
                'promocode': 'dsc10',
                'user': 'Bob',
            },
            {
                'order_id': 2,
                'address': ' Mega street',
                'promocode': 'dsc20',
                'user': 'Ben',
            },

        ]
        actual_data = response.json()['orders']
        self.assertEqual(actual_data, expected_data)


