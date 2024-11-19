from django.urls import path
from . import views

urlpatterns = [
    path('category', views.CategoryView.as_view()),
    path('menu-items', views.CategoryView.as_view()),
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),
]

