from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, AddWishlistView, RemoveWishlistView, WishlistView, ReviewCreateView, ProductReviewListView

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('products', ProductViewSet)

urlpatterns = [
    path('',include(router.urls)),
    path('wishlist/add/', AddWishlistView.as_view()),
    path('wishlist/remove/', RemoveWishlistView.as_view()),
    path('wishlist/', WishlistView.as_view()),
     path('reviews/create/', ReviewCreateView.as_view()),
    path('reviews/<int:product_id>/', ProductReviewListView.as_view()),
    
]

