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
- settings.py -> contains the application settings
- __init__.py -> defines the directory as a package
- urls.py -> contains the urls inside the application 
- wsgi.py and asgi.py -> used for deployment 

We have manage.py to manage other settings and servers in our application

To run the server use the command 

```python
python manage.py runserver 
```
