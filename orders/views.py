from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from products.models import Product, ProductVariant
from rest_framework.permissions import IsAuthenticated
from users.models import User
from rest_framework.views import APIView
from .models import Order, OrderItem, Cart, CartItem, Coupon
from .tasks import send_order_email
from .serializers import OrderSerializer
from .utils import send_email_async

# Create your views here.
class AddCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        product_id = request.data.get('product_id')
        variant_id = request.data.get('variant_id')
        quantity = int(request.data.get('quantity', 1))
        product = Product.objects.filter(id=product_id).first()
        if not product:
            return Response({"error": "Invalid product_id"}, status=400)
        variant = None
        if variant_id:
            variant = ProductVariant.objects.filter(
                id=variant_id,
                product=product   
            ).first()
            if not variant:
                return Response(
                    {"error": "Invalid variant for this product"},
                    status=400
                )
        cart, _ = Cart.objects.get_or_create(user=user)
        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            variant=variant,
            defaults={'quantity': quantity}
        )
        if not created:
            item.quantity += quantity 
            item.save()
        return Response({"message": "Added to cart"},status=status.HTTP_200_OK)
    


class RemoveFromCartView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        item_id = request.data.get('item_id')
        deleted, _ = CartItem.objects.filter(id=item_id, cart__user=request.user).delete()
        if not deleted:
            return Response({"error": "Item not found"}, status=404)
        return Response({"message": "Removed from cart"})
    
    
class UpdateCartView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        item_id = request.data.get('item_id')
        quantity = int(request.data.get('quantity'))
        item = CartItem.objects.filter(id=item_id, cart__user=request.user).first()
        if not item:
            return Response({"error": "Item not found"}, status=404)
        item.quantity = quantity
        item.save()
        return Response({"message": "Updated"})
    
    
   
class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user)
        cart_items = cart.cart_items.all() 
        if not cart_items.exists():
            return Response({"error": "Cart is empty"}, status=400)
        order = Order.objects.create(user=request.user, total_price=0, status="pending")
        total_price = 0
        for item in cart_items:
            product = item.product
            price = item.product.price
            quantity = item.quantity
            OrderItem.objects.create(
                order=order,
                product=item.product,
                variant=item.variant,
                quantity=quantity,
                price=price
            )
            total_price += price * quantity
            order.total_price = total_price
            order.save()
            
            if product.stock <= 5:
                send_email_async(
                    subject="Low Stock Alert",
                    message=f"{product.name} stock is low",
                    recipient_list=[product.vendor.user.email]
                )
        cart_items.delete()
        send_order_email.delay(order.id)
        return Response({
            "message": "Order created successfully",
            "order_id": order.id,
            "total": total_price
        })
        

class MyOrderView(APIView):
    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

      
class UserOrderListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        orders = Order.objects.filter(user=request.user).prefetch_related('item')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    
    
class UpdateOrderStatusView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, order_id):
        try:
           order = Order.objects.get(id=order_id)
           order.status = request.data.get("status")
           order.save()
           return Response({"message": "Order status updated", "status": order.status})
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)
        
    
   
class ApplyCouponView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        code = request.data.get("code")
        order_id = request.data.get("order_id")
        try:
            coupon = Coupon.objects.get(code=code, active=True)
            order = Order.objects.get(id=order_id, user=request.user)
            discount = (order.total_price * coupon.discount_percent) / 100
            order.coupon = coupon
            order.discount_amount = discount
            order.final_price = order.total_price - discount
            order.save()
            return Response({
                "message": "Coupon applied",
                "final_price": order.final_price
            })
        except Exception as e:
            return Response({"error": str(e)})
        
        
        
        
                