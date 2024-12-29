from django.shortcuts import render
from rest_framework import generics, viewsets, status
from django.contrib.auth.models import User, Group
from .models import Category, MenuItems, Cart, Order, OrderItem
from .serializers import CategorySerializer, MenuItemsSerializer, UserSerializers
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import IsManager
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
# Create your views here.
class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            permission_classes = [IsAuthenticated]
            
        return [permission() for permission in permission_classes]
    
    throttle_classes = [AnonRateThrottle, UserRateThrottle]    
    
class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItems.objects.select_related('category').all()
    serializer_class = MenuItemsSerializer
    ordering_fields = ['price']
    search_fields = ['title', 'category_title']

    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            permission_classes = [IsAuthenticated]
            
        return [permission() for permission in permission_classes]    
    
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItems.objects.select_related('category').all()
    serializer_class = MenuItemsSerializer
    
    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            permission_classes = [IsAuthenticated]
            
        return [permission() for permission in permission_classes]
    
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    
class ManagerUserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    
    def get_queryset(self):
        return User.objects.filter(groups__name='Manager')
    
    def post(self, request, *args, **kwargs):
        data = request.data
        data['groups'] = [Group.objects.get(name='Manager').id]
        serializer = UserSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    permission_classes = [IsManager]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    