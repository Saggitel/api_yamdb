from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework import routers

app_name = 'api'

urlpatterns = [
    path('v1/', include('users.urls')),
]
