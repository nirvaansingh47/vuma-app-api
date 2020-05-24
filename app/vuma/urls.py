from django.urls import path, include
from rest_framework.routers import DefaultRouter

from vuma.views import VumaRequestViewSet


router = DefaultRouter()
router.register('requests', VumaRequestViewSet)

app_name = 'vuma'

urlpatterns = [
    path('', include(router.urls))
]
