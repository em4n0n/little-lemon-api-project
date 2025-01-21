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
