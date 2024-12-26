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
    
    def validate(self,attrs):
        attrs['price'] = attrs['unit_price'] * attrs['quantity']
        return attrs
    
    class Meta:
        model = Cart
        fields = ['id', 'user', 'menuitems', 'quantity', 'unit_price', 'price']
        extra_kwargs = {
            'price': {'read_only': True}
        }
        
class OrderItemsSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'menuitem', 'quantity', 'price']
    
class OrderSerializers(serializers.ModelSerializer):
        orderitem = OrderItemsSerializers(many=True, read_only=True, source='order')
        
        class Meta:
            model = Order
            fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'date', 'orderitem']
            
class UserSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

