from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.say_hello),
    path('html/', views.html_hello),
    path('filter/', views.query_list)
]