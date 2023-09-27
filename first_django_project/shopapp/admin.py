from io import TextIOWrapper
from csv import DictReader
from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from .admin_mixins import ExportAsCSVMixin
from .models import Product, Order, ProductImage
from .forms import CSVImportForm
from django.urls import path, re_path, include
from django.shortcuts import render, redirect, get_object_or_404

class OrderInline(admin.TabularInline):
    model = Product.orders.through

class ProductInline(admin.StackedInline):
    model = ProductImage

@admin.action(description="Archive products") #функция для объявления действия, которое будет архивировать записи
def mark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=True)

@admin.action(description="Unarchive products")
def mark_unarchived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=False)


class ProductAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    actions = [
        mark_archived,
        mark_unarchived,
        "export_csv",
    ]
    inlines = [
        OrderInline,ProductInline
    ]#Для отображения связи продукта с заказом
    list_display = "pk", "name", "description_short", "price", "discount", "created_at", "archived"
    list_display_links = "pk", "name"
    ordering = "-pk",
    search_fields = "name", "description"
    fieldsets = [
        (None, {
            "fields": ("name", "description"),
        }),
        ("Price options", {
            "fields": ("price", "discount",),
            "classes": ("wide", "collapse",),
        }),
        ("Images", {
            "fields": ("preview",),
        }),
        ("Extra options", {
            "fields": ("archived",),
            "classes": ("collapse",), #т.к. tuple то добавляется запятая в скобках в конце
            "description": "Extra options. Field 'archived' is for soft delete/"
        })
    ]

    change_list_template ="shopapp/products_changelist.html"
    def import_csv(self, request: HttpRequest) -> HttpResponse:
        if request.method == "GET":
            form = CSVImportForm() # инициализация экземпляра
            context = {
                "form": form,
            }
            return render(request, "admin/csv_form.html", context)
        form = CSVImportForm(request.POST, request.FILES)
        if not form.is_valid():
            context = {
                "form": form,
            }

            return render(request, "admin/csv_form.html", context, status=400)

        #из байт получаем строчки
        csv_file = TextIOWrapper(
            form.files["csv_file"].file,
            encoding=request.encoding,
        )
        reader = DictReader(csv_file)

        products =[
            Product(**row)
            for row in reader
        ]
        Product.objects.bulk_create(products) #создаём несколько объектов сразу с помощью bulk_create
        self.message_user(request, "Data from CSV was imported") # добавляем информацию на страницу, что данные были загружены

        return redirect("..") #возвращаемся на одну страницу выше

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path(
                "import-products-csv/",
                self.import_csv,
                name="import_products_csv",
            ),
        ]
        return new_urls + urls



    def description_short(selfself, obj:Product)->str:
        if len(obj.description) < 48:
            return obj.description
        return obj.description[:48] + "...."


admin.site.register(Product, ProductAdmin)

# class OrderAdmin(admin.ModelAdmin):
#     list_display = "delivery_adress", "promocode", "created_at"
#
# admin.site.register(Order, OrderAdmin)


class ProductInline(admin.TabularInline):
    model = Order.products.through #Выводить только те сущности, которые связаны с заказом


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        ProductInline,
                ] #Для отображения всех продуктов, связанных с заказом
    list_display = "delivery_adress", "promocode", "created_at", "user"

    def get_queryset(self, request):
        return Order.objects.select_related("user").prefetch_related("products") #Prefetch.related нужен для того, чтобы подтянуть связанные сущности при переходе на страницу

    def user_verbose(self, obj:Order)->str:   # imya polzovatelia vmesto username
        return obj.user.first_name or obj.user.username



