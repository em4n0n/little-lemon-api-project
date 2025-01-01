from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from . import permissions

urlpatterns = [
    path('api-token-auth/', obtain_auth_token),
    path('category', views.CategoryView.as_view()),
    path('menu-items', views.CategoryView.as_view()),
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),
    path('groups/manager/users', views.ManagerUserView.as_view()),
    path('groups/manager/users/<int:pk>', views.ManagerUserView.as_view()),
    path('groups/delivery-crew/users', views.DeliveryCrewView.as_view()),
    path('groups/delivery-crew/users/<int:pk>', views.DeliveryCrewView.as_view()),
    path('cart/menu-items', views.CartView.as_view()),
    path('orders', views.OrderView.as_view()),
    path('orders/<int:pk>', views.SingleOrderView.as_view()),
]

