from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Order, OrderItem
from .serializers import OrderSerializer
from .permissions import IsOrderOwnerOrAdmin

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all().prefetch_related('items__product')
        return Order.objects.filter(user = self.request.user).prefetch_related('items__product')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel an order (only if pending)"""
        order = self.get_object()
        
        if order.status != 'PENDING':
            return Response(
                {'error': 'Only pending orders can be cancelled'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Restore stock
        for item in order.items.all():
            item.product.stock += item.quantity
            item.product.save()
        
        order.status = 'CANCELLED'
        order.save()
        
        serializer = self.get_serializer(order)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def my_orders(self, request):
        """Get current user's orders"""
        orders = self.get_queryset()
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)