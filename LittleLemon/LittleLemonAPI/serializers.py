from rest_framework import serializers
from .models import Category, MenuItems, Cart, Order, OrderItem
import bleach

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