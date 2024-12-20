from rest_framework import serializers
from .models import Category, MenuItems, Cart, Order, OrderItem
import bleach
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'slug']
            
class MenuItemsSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    
    def validate_title(self, value):
        return bleach.clean(value)
    
    class Meta:
        model = MenuItems
        fields = ['id', 'user', 'menuitems', 'quantity', 'unit_price', 'price', 'menuitem_id']
        
class CartSerializers(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all(),
        default = serializers.CurrentUserDefault()
    )
    
    menuitems = MenuItemsSerializer(read_only=True)
    menuitem_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Cart
        fields = ['id', 'user', 'menuitems', 'quantity', 'unit_price', 'price', 'menuitem_id']
        
class OrderSerializers(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all(),
        default = serializers.CurrentUserDefault()
    )
    
    delivery_crew = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all(),
        default = serializers.CurrentUserDefault()
    )
    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'date']