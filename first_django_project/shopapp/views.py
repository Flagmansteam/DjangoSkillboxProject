from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from timeit import default_timer

def shop_index(request:HttpRequest):
    products = [
        ('Laptop', 1999),
        ('Desktop', 2999),
        ('Smartphone', 999),
    ]
    context = {
        "time_running": default_timer(),
        "products": products,
    }
    return render(request, 'shopapp/shop-index.html', context=context)

# Create your views here.
