from django.contrib import admin, messages
from django.db.models.aggregates import Count
from django.urls import reverse
from django.utils.html import format_html, urlencode
from . import models


# Register your models here normally by
# admin.site.register(models.ModelName)

# Custom Filter definations 
class InventoryFilter(admin.SimpleListFilter):
    title = 'Inventory'
    parameter_name = 'inventory'

    def lookups(self,request,model_admin):
        return [
            ('<20', 'Low')
        ]
    
    def queryset(self,request,queryset):
        if self.value() == '<20':
            return queryset.filter(inventory__lt = 20)



# The Admin portal class
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    actions = ['clear_inventory']
    list_display = ['title', 'price', 'Inventory_Status', 'collection', 'collection_id']
    list_editable = ['price']
    # similar to select_related, just in admin panel
    list_select_related = ['collection']
    list_filter = ['collection', 'last_update', InventoryFilter]

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
    
    @admin.action(description='Clear Inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request, f'{updated_count} products were successfully updated', messages.WARNING
        )


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    ordering = ['first_name', 'last_name']
    search_fields = ['first_name', 'last_name']
    # We can use various look ups as well
    # search_fields = ['first_name__startswith', 'last_name__startswith'] # Case sensitive
    # search_fields = ['first_name__istartswith', 'last_name__istartswith'] # Case insensitive


# Registering the Orders column in Admin Portal
@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_select_related = ['customer']
    list_display = ['id', 'customer_name','placed_at','payment_status' ]
    ordering = ['placed_at']
    autocomplete_fields = ['customer']

    @admin.display(ordering='customer.first_name') # for sorting order in Admin Panel
    def customer_name(self,order):
        return order.customer.first_name+" "+order.customer.last_name

    


# The collection admin page setting to showcase how to 
# Over write the Basic Query Set 
@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'product_count']  
    # but product_count is not a defined feild inside collection, so we need to define that as well
    @admin.display(ordering = 'product_count')
    def product_count(self,collection):
        # return collection.product_count 
        # but product_count is not defined inside collection, so we need to define that as well

        # The url redirection implementation
        url = reverse('admin:shop_product_changelist')
        
        # For querying the specific products of a collection we need to add a filter
        # url += '?collection__id='+str(collection.id) # The hard-coded version of the filter
    
        # The dynamic implementation
        url += '?'+ urlencode({
            'collection__id': str(collection.id)
        })

        link = format_html('<a href={} >{}</a>',url,collection.product_count)
        return link

    def get_queryset(self, request):
        # return super().get_queryset(request) # This is the default implementation
        # Over-writing it 
        return super().get_queryset(request).annotate(
            product_count = Count('product')
        )
