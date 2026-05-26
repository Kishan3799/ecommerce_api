from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductListSerializer
from products.models import Product

class OrderItemSerializer(serializers.ModelSerializer):
    product_details = ProductListSerializer(source='product', read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.filter(is_active=True),
        source='product',
        write_only=True
    )
    subtotal = serializers.ReadOnlyField()
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product_id', 'product_details', 'quantity', 'price', 'subtotal']
        read_only_fields = ['id', 'price', 'subtotal']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'items', 'total_amount', 
                  'shipping_address', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'total_amount', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        
        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            
            # Check stock availability
            if product.stock < quantity:
                raise serializers.ValidationError(
                    f"Insufficient stock for {product.name}. Available: {product.stock}"
                )
            
            # Create order item
            OrderItem.objects.create(order=order, **item_data)
            
            # Reduce stock
            product.stock -= quantity
            product.save()
        
        # Calculate total
        order.calculate_total()
        return order