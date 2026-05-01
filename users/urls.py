from django.urls import path
from .views import LoginView, TestAuthView

urlpatterns = [
    path('api/login/', LoginView.as_view()),
    path('test-auth/', TestAuthView.as_view()),
]

