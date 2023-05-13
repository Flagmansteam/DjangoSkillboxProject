from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

def shop_index(request:HttpRequest):
    return render(request, 'shopapp/shop-index.html')

# Create your views here.
