from tkinter.font import names

from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import CustomUserViewSet, RegisterUserView, LoginView

router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='users')

urlpatterns = [
    *router.urls,
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),

]
