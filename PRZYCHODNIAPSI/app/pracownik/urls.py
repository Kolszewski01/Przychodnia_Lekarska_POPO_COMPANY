from rest_framework import routers
from .views import PracownikViewSet, LekarzViewSet
from django.urls import include, path

router = routers.DefaultRouter()
router.register(r'pracownik', PracownikViewSet)
router.register(r'lekarz', LekarzViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),  # Poprawiono średnik na myślnik
]