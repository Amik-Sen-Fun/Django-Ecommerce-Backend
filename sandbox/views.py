from django.shortcuts import render
from django.http import HttpResponse

from shop.models import Product

# Create your views here.
def say_hello(request):
    return HttpResponse("Hello World")

def html_hello(request):
    return render(request, 'hello.html', {'name': 'Amik'})

def query_list(request):
    query_set = Product.objects.filter(price__range=(20,30))
    return render(request, 'query_list.html', {'product': list(query_set)})

def related_list(request):
    query_set = Product.objects.select_related('collection').all()
    return render(request, 'related.html', {'products': list(query_set), 'user': 'Amik'})