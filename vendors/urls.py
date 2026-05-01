from django.urls import path
from .views import BecomeVendorView, ApproveVendorView, VendorDashboardView

urlpatterns = [
    path('become-vendor/', BecomeVendorView.as_view()),
    path('approve/<int:vendor_id>/', ApproveVendorView.as_view()),
    path('dashboard/', VendorDashboardView.as_view()),
]


