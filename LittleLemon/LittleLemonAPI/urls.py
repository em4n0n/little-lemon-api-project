from django.urls import path
from . import views

urlpatterns = [
    path('category', views.CategoryView.as_view()),
    path('menu-items/<int:pk>', views.SingleMenuView.as_view()),
]

