"""

В этом модуле лежат различные наборы представлений.

Разные view интернет-магазина: по товарам, заказам и т.д.

"""
from csv import DictWriter
import logging
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from timeit import default_timer
from rest_framework.parsers import MultiPartParser #позвоялет парсить то, что мы передали в виде файлов, потому что в джанго по умолчанию установлен json парсер
from django.contrib.auth.models import Group
from .common import save_csv_products
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Product, Order, ProductImage
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin # позволяет создать любую функцию для проверки
from django.contrib.auth.models import User
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action # можно поключить любую новую вью функцию к вью сету
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import ProductSerializer, OrderSerializer
from drf_spectacular.utils import  extend_schema, OpenApiResponse
from django.contrib.syndication.views import Feed

log = logging.getLogger(__name__) # стандартный формат создания нового логгера


@extend_schema(description ="Products views CRUD")
class ProductViewSet(ModelViewSet):
    """

    Набор представлений для действий над Product.

    Полный CRUD для сущностей товара

    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends =[
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = ["name","description"]
    filterset_fields = [
        "name",
        "description",
        "price",
        "discount",
        "archived",
    ]
    ordering_fields = [
        "name",
        "description",
        "price",
    ]

    @action(methods=["get"], detail=False) #путь к download_csv должен быть построен на основе адреса для списка элементов
    def download_csv(self, request:Request):
        response = HttpResponse(content_type="text/csv")  # объект, в который будут выводиться данные
        filename = "products-export.csv"
        response["Content-Disposition"] = f"attachment;filename={filename}"
        queryset = self.filter_queryset(self.get_queryset())
        fields = [
            "name",
            "description",
            "price",
            "discount",
        ]

        queryset = queryset.only(*fields) # only сделает загрузку только избранных полей
        writer = DictWriter(response, fieldnames=fields)
        writer.writeheader()

        for product in queryset:
            writer.writerow({
                field: getattr(product,field)
                for field in fields
            })

        return response

    # для реализации возможности загрузить товары через action
    @action(
        detail=False,
        methods=["post"],
        parser_classes=[MultiPartParser]
    )
    def upload_csv(self):
        products = save_csv_products(
            request.FILES["file"].file,
            encoding=request.encoding,
        )
        serializer = self.get.serializer(products, many=True)
        return Response(serializer.data) # вернёт объект, который легко преобразуетсяк json



    @extend_schema(
        summary="Get one product by ID",
        description="Retrieves product,returns 404 if not found",
        responses={
            200:ProductSerializer,
            404:OpenApiResponse(description="Empty response product by ID not found"),
        }
    )
    def retrieve(self,*args,**kwargs):
        return super().retrieve(*args,**kwargs)



class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends =[
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = ["delivery_adress","description","products", "user", "promocode",]
    filterset_fields = ["delivery_adress","description","products", "user", "promocode",]
    ordering_fields = ["delivery_adress","description","products", "user", "promocode",]

class ShopIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        products = [
            ('Laptop', 1999),
            ('Desktop', 2999),
            ('Smartphone', 999),
        ]
        context = {
            "time_running": default_timer(),
            "products": products,
            "items": 5,
        }
        log.debug("Products for shop index: %s", products) # передаём правило для форматирования
        log.info("Rendering shop index")
        return render(request, 'shopapp/shop-index.html', context=context)


class GroupsListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            "form": GroupForm(),
            "groups": Group.objects.prefetch_related('permissions').all(),
        }
        return render(request, 'shopapp/groups-list.html', context=context)

    def post(self, request: HttpRequest):
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect(request.path)


class ProductDetailsView(DetailView):
    template_name = "shopapp/products-details.html"
    # model = Product
    queryset = Product.objects.prefetch_related("images")
    context_object_name = "product"



class ProductsListView(ListView):
    template_name = "shopapp/products-list.html"
    # model = Product
    context_object_name = "products"
    queryset = Product.objects.filter(archived=False)


def create_product(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            # name = form.cleaned_data["name"]
            # Product.objects.create(**form.cleaned_data)
            form.save()
            url = reverse("shopapp:products_list")
            return redirect(url)
    else:
        form = ProductForm()
    context = {
        "form": form,
    }
    return render(request, "shopapp/create-product.html", context=context)


def create_order(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            url = reverse("shopapp:order-list")
            return redirect(url)
    else:
        form = OrderForm()
    context = {
        "form": form,
    }
    return render(request, "shopapp/create-order.html", context=context)


def categories(request, catid):
    return HttpResponse(f"<h1> Test categories </h1><p>{catid}</p>")


def archive(request, year):
    return HttpResponse(f"<h1> Archive</h1><p>{year}</p>")


class ProductCreateView(UserPassesTestMixin,CreateView):
    def test_func(self):
        if self.request.user.is_superuser or self.request.user.has_perm('shopapp.add_product'):
            return True
        return False

    # model = Product
    queryset = Product.objects.prefetch_related("images")
    fields = "name", "price", "description", "discount", "preview"
    success_url = reverse_lazy("shopapp:products_list")
    def form_valid(self,form): # переопределяем метод для создания продукта, чтобы установить текущее значение created by текущему пользователю
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    def test_func(self):
        if self.request.user.is_superuser or self.request.user.has_perm("shopapp.product_update_form") or product.author == self.request.user:
            return True
        return False

    model = Product
    # fields = "name", "price", "description", "discount", "preview"
    template_name_suffix = "_update_form"
    form_class = ProductForm
    def get_success_url(self):
        return reverse(
            "shopapp:product_details",
            kwargs={"pk": self.object.pk},
        )

    def form_valid(self, form):
        response = super().form_valid(form)
        for image in form.files.getlist("images"):
            ProductImage.objects.create(
                product=self.object,
                image=image,
            )

        return response

class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)




# class OrderListView(ListView):
#     template_name = "shopapp/order_list.html"
#     model = Order
#     context_object_name = "object_list"



class OrderListView(LoginRequiredMixin, ListView):
    queryset = (
        Order.objects
        # .select_related("user")
        # .prefetch_related("products")
        .all()
    )

# class OrderDetailView(DetailView):
#     template_name = "shopapp/order_detail.html"
#     model = Order
#     context_object_name = "object_list"


class OrderDetailView(PermissionRequiredMixin,DetailView):
    permission_required = "view_order"
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )

class OrderCreateView(CreateView):
    model = Order
    fields = "delivery_adress", "promocode", "products", "user"
    success_url = reverse_lazy("shopapp:order_list")


class OrderUpdateView(UpdateView):
    model = Order
    fields = "delivery_adress", "promocode", "products", "user"
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "shopapp:order_detail",
            kwargs={"pk": self.object.pk},
        )

class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy("shopapp:order_list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


#декоратор login_required для того, чтобы требовать аутентификацию пользователей перед созданием продукта.

class ProductsDataExportView(View):
    def get(self, request: HttpRequest)-> JsonResponse:
        products = Product.objects.order_by("pk").all()
        products_data = [
            {
                "pk": product.pk,
                "name": product.name,
                "price": product.price,
                "archived": product.archived,
            }
            for product in products
        ]

        elem = products_data[0]

        # name = elem["name"]
        name = elem["name"]
        print("name:", name)

        return JsonResponse({"products": products_data})



class OrdersDataExportView(UserPassesTestMixin, View):
      def test_func(self):
          return self.request.user.is_staff

      def get(self, request):
          orders = Order.objects.order_by("pk").all()
          orders_data = [
              {
                  'order_id': order.id,
                  'address': order.delivery_adress,
                  'promocode': order.promocode,
                  'user': order.user,
              }
              for order in orders
          ]
          return JsonResponse({"orders": orders_data})




class LatestProductsFeed(Feed):
    title = "Products (latest)"
    description = "Updates on changes and addition products"
    link = reverse_lazy("shopapp:products_list")

    def items(self):
        return(
            Product.objects
            .filter(created_at__isnull=False)
            .order_by("-created_at")[:20]
        )

    def product_name(self, product: Product):
        return product.name

    def product_description(self, product: Product):
        return product.description[:200]


    def item_link(self, item: Product):
        return reverse("shopapp:products_list", kwargs={"pk":item.pk})