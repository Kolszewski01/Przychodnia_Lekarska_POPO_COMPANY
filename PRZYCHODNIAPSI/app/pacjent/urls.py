from rest_framework import routers
from .views import PacjentViewSet
from django.urls import include, path


router = routers.DefaultRouter()
router.register(r'pacjent', PacjentViewSet)
app_name = 'pacjent'

urlpatterns = [
    path('api/', include(router.urls)),
    path('api_auth/', include('rest_framework.urls', namespace='rest_framework')),

]