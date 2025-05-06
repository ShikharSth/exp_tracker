from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CustomTokenObtainPairView, IncomeViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'incomes', IncomeViewSet, basename='incomes')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
]