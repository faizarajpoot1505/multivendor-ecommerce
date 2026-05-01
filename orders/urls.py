from django.urls import path
from .views import AddCartView, RemoveFromCartView, UpdateCartView, CreateOrderView, UserOrderListView, UpdateOrderStatusView, ApplyCouponView


urlpatterns = [
    path('cart/add/', AddCartView.as_view()),
    path('cart/remove/', RemoveFromCartView.as_view()),
    path('cart/update/', UpdateCartView.as_view()),
    path('create/', CreateOrderView.as_view()),
    path('my-orders/', UserOrderListView.as_view()),
    path('update-status/<int:order_id>/', UpdateOrderStatusView.as_view()),
    path('apply-coupon/', ApplyCouponView.as_view()),
]

