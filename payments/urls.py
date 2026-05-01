from django.urls import path
from .views import  stripe_webhook, CreateCheckoutSessionView

urlpatterns = [
    path('checkout/', CreateCheckoutSessionView.as_view()),
    path('webhook/', stripe_webhook),
]
