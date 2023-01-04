from django.db import models

# Create your models here.

# Defining Collection 
class Collection(models.Model):
    title = models.CharField(max_length=255)


class Promotions(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField(default=0)


# Defining the Product class which will be used to create object
class Product(models.Model):
    # By default Django creates an ID, to avoid this define a primary key as shown in next line 
    # sku = models.CharField(max_length= 10, primary_key = True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True) # To update everytime
    # use auto_now_add -> to only update when the object is created for the first time 

    # many to one relationship
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)

    # many to many relationship
    promotions = models.ManyToManyField(Promotions, related_name="products")
    # In many-to-many relationship Django will create a filed in Promotions as well to store product set
    # This field name can be changed using `related_name`



# THE CUSTOMER  model to define the customer object
class Customer(models.Model):
    PRIME_MEMBER = 'P'
    REGULAR_MEMBER = 'R'

    # Choice Filed options
    MEMBERSHIP_CHOICES = [
        (PRIME_MEMBER,'Prime'),
        (REGULAR_MEMBER, 'Regular')
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True) # for checking uniqueness of email field
    phone = models.IntegerField() # phone numbers are 10 digit only 
    birth_date = models.DateTimeField(null=True)

    # Choice feild
    membership = models.CharField(choices=MEMBERSHIP_CHOICES, default= REGULAR_MEMBER, max_length=1)
    
    
   

# The order class to define an order
class Order(models.Model):

    COMPLETE_STATUS = 'C'
    PENDING_STATUS = 'P'
    FAILED_STATUS = 'F'

    PAYMENT_STATUS = [
        (COMPLETE_STATUS, 'Complete'),
        (PENDING_STATUS, 'Pending'),
        (FAILED_STATUS, 'Failed')
    ]

    placed_at = models.DateTimeField(auto_now_add=True) # We don't want to change the value every time
    payment_status = models.CharField(max_length=1, choices = PAYMENT_STATUS, default=PENDING_STATUS)

    # many to one relationship
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

# Defining an address class
class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)

    # Here we are assuming that one customer has only one address
    # So customer is the parent class and address is a child class as address exists only when a customer exits
    # So the child will have a reference to the parents

    customer = models.OneToOneField(Customer, primary_key = True ,on_delete=models.CASCADE) # Primary key works because it's one to one 
    # CASCADE means once a parent is deleted the child will also be deleted. Customer DELETED => Address DELETED
    # SET_NULL can also be used. If parent is deleted the child will be labelled as NULL and not deleted
    # SET_DEFAULT can be used to use a default value 
    # PROTECT is used to disable deletion of parent. First child need to be deleted and parent. 
    
    # To define a one to many relationship do 
    # customer = models.ForeignKey(Customer, on_delete=models.CASCADE)


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)  # No need to keep this order items if order is deleted
    products = models.ForeignKey(Product, on_delete=models.PROTECT) # PROTECT this order even if product is now deleted
    quantity = models.PositiveSmallIntegerField()
    unitPrice = models.DecimalField(max_digits=6, decimal_places=2)

class CartItem(models.Model):
    items = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

