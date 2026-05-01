from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.models import User
from .models import Vendor
from orders.models import Order, OrderItem
from products.models import Product
from django.db.models import Sum, Count


class BecomeVendorView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        vendor, created = Vendor.objects.get_or_create(
            user=request.user,
            defaults={"shop_name": request.user.username}
        )
        vendor.is_approved = False
        vendor.save()
        return Response({"message": "Request sent for approval"})
    
    
    
class ApproveVendorView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, vendor_id):
        if request.user.role != 'admin':
            return Response({"error": "Only admin allowed"}, status=403)

        vendor = Vendor.objects.get(id=vendor_id)
        vendor.is_approved = True
        vendor.save()

        return Response({"message": "Vendor approved"})
    
    

class VendorDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        vendor = Vendor.objects.get(user=request.user)
        products = Product.objects.filter(vendor=vendor)
        order_items = OrderItem.objects.filter(product__vendor=vendor)
        orders = Order.objects.filter(item__product__vendor=vendor).distinct()
        total_sales = Order.objects.aggregate(total=Sum('total_price'))
        total_orders = Order.objects.aggregate(count=Count('id'))
        if not vendor.is_approved:
            return Response({"error": "Vendor not approved yet"})
        return Response({
            "vendor": str(vendor),
            "total_products": products.count(),
            "total_order_items": order_items.count(),
            "total_orders": orders.count(),
            "total_sales": total_sales,
            "total_orders": total_orders,
        })
        
        
        
        
        
        