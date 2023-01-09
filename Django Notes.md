# Django Tutorial

## What is Django?

- It is a free open source python framework to develop web application
- It is very popular
- comes with lots of inner features like ORM, admin panel, Authentication, Caching

## Web Dev Basics

- Application comes with a frontend (client) and backend (server)
- The link which takes a user to our website is called a URL (Uniform Resource Locator)
- Server takes a request from the client side and send a response.
  - This exchange is monitored by a protocol known as HTTP ( Hyper Text Transfer Protocol )
- The Website show the rendered HTML file, which can be either sent by the server or can be there at the client side
- Usually servers are built with end points for API (Application Programming Interface) calls, which increases scalability

## Virtual Environement Setup

Since we might be installing some packages and stuff it is better to maintain those files in a virtual environment and work with them.

To install the python3 virtual environment type the following code in terminal

```
python3 -m pip install --user --upgrade pip
python3 -m pip --version # to check the pip version
python3 -m pip install --user virtualenv
```

To create a virtual environment for a project:

```
python3 -m venv env_name
// Try to keep this in .gitignore file
```

To activate the virtial env type:

```
source env_name/bin/activate
```

To deactivate the virtual env type:

```
deactivate
```

## First Django project

To create the first project, use coomand

```python
django-admin startproject store
# This will create a new directory named 'store' and store files inside it

django-admin startproject store .
# This is use the current directory as the parent directory and not create the 'store' folder again
```

The files that are created are the core of our application:

- `settings.py` -> contains the application settings
- `__init__.py` -> defines the directory as a package
- `urls.py` -> contains the urls inside the application
- `wsgi.py` and `asgi.py` -> used for deployment

We have manage.py to manage other settings and servers in our application

To run the server use the command

```python
# The following command runs the django server on port 8000
python manage.py runserver

# To run the django server on some other port say 9000 do
python manage.py runserver 9000
```

## First Django application

Inside each django project we can create multiple applications. Some of the predefined applications can be found in `settings.py` under `INSTALLED_APPS` as following :

- `django.contrib.admin` : Provides the admin panel
- `django.contrib.messages` : Provides one time messages for the users
- `django.contrib.sessions` : Sessions application used to store session info in server. It is not used now (JWT can be used)
- `django.contrib.auth` : This is the authentication module provided by Django
- `django.contrib.contenttypes` : Used to create generic relationship in our models. (Refer models of Tags)
- `django.contrib.staticfiles` : Used to serve static files like images, pdfs, videos etc

To make create your own application, write :

```python
python manage.py startapp sandbox # sandbox is the application name
```

Inside the app `sandbox`, we have the following files:

- `migrations`
- `apps.py` - Contains the configurations of this application
- `admin.py` - To know which models to show in the admin portal
- `models.py` - Model classes are defined here, which are used to extract data from the database
- `test.py` - used to run tests on the application
- `views.py` - Request handler

> Everytime we create a new application we need to add it to the `INSTALLED_APPS` section in `settings.py`. In this case write `, sandbox` after the last application name

## How to write views?

A view takes in a request and sends a response. So, it's basically a request handler. An example of a view is :

```python
from django.http import HttpResponse

def say_hello(request):
  return HttpResponse('Hello world')
```

Now if we wanna map urls to our views we need to do the following steps:

- Inside the `sandbox` folder, define a file named `urls.py` and write the following:

  ```python
  from django.urls import path
  from . import views

  urlpatterns = [
    path('hello/', views.say_hello)
  ]
  ```

- Now we need to include these urls with the main application urls, this is done by going in the `store` folder and writing the following commands in `urls.py` (store):

  ```python
  from django.contrib import admin
  from django.urls import path, include

  urlpatterns = [
      path('admin/', admin.site.urls),
      path('sandbox/', include('sandbox.urls')),
  ]
  ```

## Templates

We can render HTML files in Django as well, for that we create a folder named `templates` inside `sandbox` and define HTML files.

To render these HTML files:

```python
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def say_hello(request):
    return render(request,'hello.html')

# refer to code for seeing the HMTL template and custom django templates
```

## How to debug Django Code in VS Code

- Go to the debugger -> creata a `launch.json` file for Django
- You can also google and use `Django Debug Toolbar` and download it using

  ```python
  python -m pip install django-debug-toolbar
  ```

  Then mention it in the `settings.py` file of the project as `debug_toolbar`, put in the `urls.py` and in `MIDDLEWARE` and `INTERNAL_IPS` in `settings.py` file as mentioned in the docs and this code

> Django Debug Toolbar is really cool :p

## Making the E-commerce Data model

First we will define models like Product, categories and define relationships between them

There are many kinds of relationships possible between entities such as:

- One to One
- Many to Many
- One to Many

For the product and category, A category can have many products so it's a many to one relationship.

> Note: In Django IDs are automatically created
> Always make models based on the requirements

Now in order to make scalable application it is a good practice to make each component as an application.

For our application we can have an application and define model inside it such as product, category, cart, order, custormers etc. ( This is known as a Monolith, making it hard to make changes and understand ) but in order to make a scalable product we define seperate applications such as:

- Product
  - Models: Item, Category, Tag
- Customer
  - Models: Customer
- Carts
  - Models: Cart, CartItem
- Orders
  - Models: Order, OrderItem

However, any change in the Product will mean changes in the Carts and Orders as they are related, so breaking a big application into too many small applications is also a headache.

So, we will go for a middle ground. Only Tags is an independent module. So, we will make it as a seperate application. This way we are ensuring

- Zero coupling
- Self containtment

Hence proceeding with two application `shop` and `tags`.

Inside `shop` now we will define models, refer the code for that. One example is given below as the `Product` model:

```python
from django.db import models

# Create your models here.

# Defining the Product class which will be used to create object
class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True) # To update everytime
    # use auto_now_add -> to only update when the object is created for the first time
```

- Important concepts and applications (Read comments)
  - Choice fields : See `Customer` models in `shop`
  - Defining **one-to-one** relationships: See `Address` model in `shop` (models.OneToOneField())
  - Defining **one-to-many** relationships: See `Address` model in `shop` (models.ForeignKey())
  - Defining **many-to-many** relationships: See `Promotions` and `Products` model in `shop` (models.ManyToManyField())
  - Defining **circular dependency** : To give the `featured_products` see `collection` model in `shop`
  - **Generic Relationships** : Models in `tags` application

## Migrations

- To save a new model or save changes in existing models do

  ```python
  python manage.py makemigrations
  ```

> If you have made changes in a model and the above command shows no changes detected => make sure you written app in **INSTALLED_APPS** in `settings.py`

> NOTE: Slug is a search engine optimisation technique

- To reflect changes in DB do,
  ```python
  python manage.py migrate
  ```
- To reflect changes in DB and see the SQL codes do,
  ```python
  python manage.py sqlmigrate shop 0003
  ```

### Customize Database Schema

For this we define a class `Meta` inside the defined models (See `customer` in `shop`)

```python
# Meta data class
   . . . . . .
    class Meta:
        db_table = 'store_customers'
        # VERBOSE is also some META field, see documentation
        indexes = [
            models.Index(fields = ['last_name', 'first_name'] )
        ]
    . . . .
```

To revert a migration:

```python
python manage.py migrate shop 0003 # Say you are at 0004 and want to revert back to 0003
```

> Note: However, after this revert, the migration file still remains, so if you migrate still it will be migrated so delete it. Also delete the code which you wanna undo ( Maybe use version control for it :p )

For this project we will be using the default sqlite db but if you wanna connect to another database do the following steps :

### For connecting mysql

- first install `mysqlclient` through `pip`
  ```python
  pip install mysqlclient
  ```
- In the `settings.py` of the main project in the `DATABASES` section give the following information

````python
# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':  'user',
        'USER': 'app',
        'PASSWORD': '1234',
        'HOST': 'localhost',
    }
}

### For connecting postgresql

- In the `settings.py` of the main project in the `DATABASES` section give the following information

```python
# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME':  'user',
        'USER': 'app',
        'PASSWORD': '1234',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
````

### For running custom SQL queries

- Make an empty migration by:
  ```python
  python manage.py makemigrations shop --empty
  ```
- Inside the empty migration wite the SQL command as:

  ```python
  # Generated by Django 4.1.5 on 2023-01-05 13:50
  from django.db import migrations

  class Migration(migrations.Migration):

      dependencies = [
          ('shop', '0002_customer_store_custo_last_na_e6a359_idx_and_more'),
      ]

      operations = [
          # Custom SQL query here
          migrations.RunSQL("""
            SELECT * FROM shop;
          """, """

          """)
          # Fist argument of RunSQL() is for updating the database
          # Second argument is optional which is used for downgrading the database (Like from INSERT -> DELETE)
      ]

  ```

  > For Generating Dummy Data we can use `mockaroo.com`

## Django ORM (Object Relational Mapper)

ORMs are used to map SQL queries to objects. So that we don't need to write many SQL codes. They don't do good with complex queries though.

- Demerits of ORM :

  - A bit slow than raw SQL queries

- Merits of ORM :
  - We need to less code which requires less maintenance, and hence cost less money

## Managers and querysets

Say Product is a class defined in models.py then consider the following:

- If we do `Product.objects` it returns a _manager instance_ which is used to fetch data from the database

- Some basic query syntax:
  |Syntax|Function|
  |---|---|
  |`Product.object.all()`|fetches all data from table Product|
  |`Product.object.get()`|for getting a single object (doesn't return a query set)|
  |`Product.object.filter()`|used to get filtered data|
  |`Product.object.order_by()`|used to rearrange the data|

- But these functions return a **query set**, Django fetches the actual data when we do some operation on this query set, like :

  - _itterate over it_
  - _convert it to a list_
  - _slicing the query set_
    This is known as _lazy_ feature of Django, which is done so that we can process complex queries.

- Some manager commands don't return a query set like _count()_ function, because it is a number, no further complex query can be executed here.

### Retriving Objects in Django ORM

- `Product.object.all()` is used to retrieve all objects from the database.
- `Product.object.get(id=1)` is used to get a single object with id = 1
- `Product.object.get(pk=1)` is used to get a single object having the primary key = 1

With the `get()` filter if we don't get any value the application will throw an exception. For this we will use the try and except block as:

```python
from django.core.exceptions import ObjectDoesNotExist

try:
  product = Product.object.get(id=1)
except ObjectDoesNotExist:
  pass
```

or we can remove the try and catch exception by

```python
product = Product.object.filter(id=1).first()
# This will store None in product if nothing is present
# Or we can write
if Product.object.filter(id=1).exists():
  pass
# exists() returns a boolean value
```

### Filtering Objects in Django ORM

The `filter()` method takes in a keyword value and filters data accordingly:

- `Product.object.filter(unit_price = 20)` - Returns a query set with object having `unit_price` = 20

> However in the `filter()` method we cannot use logical operators like <,>, or =

For logical comparison we need to write syntax as:

- `Product.object.filter(unit_price__gt = 20)` - Returns a query set with object having `unit_price` > 20

> For other such `lookups` google them

- We can also filter cross relational data by :
  `Product.object.filter(collection__id__gt = 20)` - Returns a query set with object having `collection` with `id` greater than 20.

- To filter using string we write as follows:

  - `Product.object.filter(title__contains = 'coffee')` - Returns a query set with object having title containing `coffee` and this is case sensitive. To make this case insensitive use `__icontains()`
  - `Product.object.filter(title__startswith = 'coffee')`
  - `Product.object.filter(title__endswith = 'coffee')`

- To filter using dates we write as follows:

  - `Product.object.filter(last_update__year = 2010)`

- To check null values:
  - `Product.object.filter(description__isnull = True)`

### Complex lookups using query objects

- We wanna lookup _products having inventory < 10 AND price >20_, we can achieve this by:

  - `Product.object.filter(inventory__lt = 10, price__gt = 20)` - uses an AND SQL command
  - `Product.object.filter(inventory__lt = 10).filter(price__gt = 20)` - same as before

- We wanna lookup _products having inventory < 10 OR price >20_, for this we need to import `Q`:

  ```python
  from django.db.models import Q

  products = Product.object.filter(Q(inventory__lt = 10)| Q(price__gt = 20))

  # For AND in Q operator use &
  # For NOT in Q operator use ~
  ```
