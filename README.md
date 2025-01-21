# Little Lemon 🍋

**Little Lemon** is a RESTful API designed for a restaurant, offering a range of functionalities for both admins and customers. This project was developed with the help of coursework from Coursera's Meta Backend Developer API course.

## Features

- **Role-Based Access Control** 🔒: Manage users, menu items, categories, and delivery crew assignments.
- **Customer Interactions** 👥: Allow customers to register, log in, browse the menu, manage their cart, place orders, and track orders with pagination and sorting.
- **RESTful API** 🌐: Provides endpoints for all major functionalities.

# Clone project
```bash
git init
git clone https://github.com/em4n0n/little-lemon-api-project
cd LittleLemon
```

## Install pipenv
```bash
pip3 install pipenv
```

## Activate virtual environment
```bash
pipenv --python 3.12
pipenv shell
```

## Install Django & frameworks
```bash
# Django
pipenv install django

# Frameworks
pipenv install djangorestframework
pipenv install django-debug-toolbar
# pipenv install djangorestframework-xml
pipenv install bleach
pipenv install djoser
# pipenv install djangorestframework-simplejwt
```

# Run server
```bash
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```

# API endpoints
## Account required
```bash
Admin
    username: admin
    password: useradmin123!@#

Delivery crew
    username: joedoe
    password: userjoedoe123!@#

Manager
   username: janedoe
   password: userjanedoe123!@#

Customer
    username: customer
    password: usercustomer123!@#
```

```bash
/auth/users
/auth/users/me/
/auth/token/login/
```

## Menu-items
```bash
/api/menu-items
/api/menu-items/<int:pk>
```

## User group management
```bash
/api/groups/manager/users
/api/groups/manager/users/<int:pk>
```

```bash
/api/groups/delivery-crew/users
/api/groups/delivery-crew/users/<int:pk>
```

## Cart management
```bash
/api/cart/menu-items
```

## Order management
```bash
/api/orders
/api/orders/<int:pk>
```

## Deactivate virtual environment
```bash
exit
```
