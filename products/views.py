from rest_framework import viewsets
from .models import Category, Product, Wishlist, Review
from .serializers import CategorySerializer, ProductSerializer, WishlistSerializer, ReviewSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, permissions


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    
class WishlistView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        wishlist = Wishlist.objects.filter(user=request.user)
        serializer = WishlistSerializer(wishlist, many=True)
        return Response(serializer.data)
   
    
class AddWishlistView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        product_id = request.data.get("product_id")
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)
        wishlist, created = Wishlist.objects.get_or_create(user=user, product=product)

        return Response({"message": "Added to wishlist"})


class RemoveWishlistView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        product_id = request.data.get("product_id")
        Wishlist.objects.filter(user=user, product_id=product_id).delete()

        return Response({"message": "Removed from wishlist"})
    
    
class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        product_id = self.request.data.get('product')
        product = Product.objects.get(id=product_id)
        serializer.save(
            user=self.request.user,
            product=product
        )
        
        
 
class ProductReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return Review.objects.filter(product_id=product_id)
    
    
    
    
 