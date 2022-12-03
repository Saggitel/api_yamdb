from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import UserViewSet, RegistrationView, CreateTokenView

app_name = 'users'

router_v1 = routers.DefaultRouter()
router_v1.register(r'users', UserViewSet, basename='users')


urlpatterns = [
    path('auth/token/', CreateTokenView.as_view(), name='create_token'),
    path('auth/signup/', RegistrationView.as_view(), name='registration'),
    path('', include(router_v1.urls)),
]