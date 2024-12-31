from django.shortcuts import render, get_objects_or_404
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
        manager_group = Group.objects.get(name='Manager')
        return User.objects.all().filter(groups=manager_group)
    
    def post(self, request, *args, **kwargs):
        username = request.data.get['username']
        if username:
            user = get_objects_or_404(User, username=username)
            manager_group = Group.objects.get(name='Manager')
            manager_group.user_set.add(user)
            return Response({'status': 'User added to Manager group'}, status=status.HTTP_201_CREATED)
        return Response({'status': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            
    
    permission_classes = [IsManager]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    
class SingleMangerUserView(generics.RetrieveDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    
    def get_queryset(self):
        manager_group = Group.objects.get(name='Manager')
        return User.objects.all().filter(groups=manager_group)
    
    def delete(self, request, *args, **kwargs):
        username = request.data.get['username']
        if username:
            user = get_objects_or_404(User, username=username)
            manager_group = Group.objects.get(name='Manager')
            manager_group.user_set.remove(user)
            return Response({'status': 'User removed from Manager group'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'status': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    permission_classes = [IsManager]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]