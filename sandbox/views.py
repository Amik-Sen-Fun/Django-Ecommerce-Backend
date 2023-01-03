from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def say_hello(request):
    return HttpResponse("Hello World")

def html_hello(request):
    return render(request, 'hello.html', {'name': 'Amik'})