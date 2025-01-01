from django.shortcuts import render, get_objects_or_404
from rest_framework import generics, viewsets, status
from django.contrib.auth.models import User, Group
from .models import Category, MenuItems, Cart, Order, OrderItem
from .serializers import CategorySerializer, MenuItemsSerializer, UserSerializers, CartSerializers, OrderSerializers
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
    
class DeliveryCrewView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    
    def get_queryset(self):
        delivery_crew_group = Group.objects.get(name='Delivery Crew')
        return User.objects.all().filter(groups=delivery_crew_group)
    
    def post(self, request, *args, **kwargs):
        username = request.data.get['username']
        if username:
            user = get_objects_or_404(User, username=username)
            delivery_crew_group = Group.objects.get(name='Delivery Crew')
            delivery_crew_group.user_set.add(user)
            return Response({'status': 'User added to Delivery Crew group'}, status=status.HTTP_201_CREATED)
        return Response({'status': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            
    
    permission_classes = [IsManager]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    
class SingleDeliveryCrewView(generics.RetrieveDestroyAPIView):
    serializer_class = UserSerializers
    
    def get_queryset(self):
        return User.objects.filter(groups__name="Delivery Crew")
    
    def delete(self, request, *args, **kwargs):
        username = request.data.get['username']
        if username:
            user = User.objects.filter(username=username).first()
            if user:
                delivery_crew_group = Group.objects.get(name="Delivery Crew")
                delivery_crew_group.user_set.remove(user)
                return Response({'status': 'User removed from Delivery Crew group'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'status': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
class CartView(generics.ListCreateAPIView, generics.DestroyAPIView):
    serializer_class = CartSerializers
    permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_queryset(self):
        # Filter the cart items for the current authenticated user
        return Cart.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        # Delete all cart items for the current user
        self.get_queryset().delete()
        return Response({'Message': 'Items have been deleted.'}, status=status.HTTP_204_NO_CONTENT)

class OrderView(generics.ListCreateAPIView):
    serializer_class = OrderSerializers
    permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Order.objects.all()
        if user.groups.filter(name='delivery crew').exists():
            return Order.objects.filter(delivery_crew=user)
        return Order.objects.filter(user=user)

    def post(self, request, *args, **kwargs):
        cart_items = Cart.objects.filter(user=self.request.user)
        if cart_items.exists():
            total = sum(item.price for item in cart_items)
            order = Order.objects.create(user=self.request.user, total=total)
            order_items = [
                OrderItem(order=order, item=item.item, quantity=item.quantity)
                for item in cart_items
            ]
            OrderItem.objects.bulk_create(order_items)
            cart_items.delete()
            return Response({'Message': 'Order has been placed.', 'Total': total}, status=status.HTTP_201_CREATED)
        return Response({'Message': 'Cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)
    
class SingleOrderView(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializers
    permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def update(self, request, *args, **kwargs):
        # Restrict update if the user does not belong to any group
        if not self.request.user.groups.exists():
            return Response({'detail': 'Not authorized to update this order.'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)