from django.contrib import admin
from . import models

# The Admin portal class
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'Inventory_Status', 'collection', 'collection_id']
    list_editable = ['price']
    # similar to select_related, just in admin panel
    list_select_related = ['collection']

    # We cannot directly access the collection id as Collection will return it's string representation 
    # Which is title in our case, so we have to define an seperate method
    def collection_id(self,product):
        return product.collection.id
    # however, this might lead to extra queries and increase the application time so to reduce that
    # we can preload the tables, just like select_related


    @admin.display(ordering='inventory') # for sorting order in Admin Panel
    def Inventory_Status(self, product):
        if product.inventory<20:
            return 'Low'
        return 'Ok'

# Register your models here.
admin.site.register(models.Collection)

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    ordering = ['first_name', 'last_name']


# Registering the Orders column in Admin Portal
@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_select_related = ['customer']
    list_display = ['id', 'customer_name','placed_at','payment_status' ]
    ordering = ['placed_at']

    @admin.display(ordering='customer.first_name') # for sorting order in Admin Panel
    def customer_name(self,order):
        return order.customer.first_name+" "+order.customer.last_name