import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from orders.models import Order
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        order = Order.objects.filter(user=user).last()
        if not order:
            return Response({"error": "No order found"}, status=400)
        if order.total_price <= 0:
            return Response({"error": "Invalid order amount"}, status=400)
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': f'Order #{order.id}',
                            },
                            'unit_amount': int(order.total_price * 100),
                        },
                        'quantity': 1,
                    }
                ],
                mode='payment',
                success_url='http://127.0.0.1:8000/success/',
                cancel_url='http://127.0.0.1:8000/cancel/',
                metadata={
                    "order_id": str(order.id)
                }
            )
            return Response({
                "checkout_url": session.url
            })
        except Exception as e:
            return Response({"error": str(e)}, status=400)
        
        
        
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except Exception as e:
        print("WEBHOOK ERROR:", e)
        return HttpResponse(status=400)
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        order_id = session.get('metadata', {}).get('order_id')
        if order_id:
            try:
                order = Order.objects.get(id=order_id)
                order.status = 'confirmed'
                order.save()
            except Order.DoesNotExist:
                print("Order not found")
    return HttpResponse(status=200)



