from rest_framework import routers
from .views import WizytaViewSet, ParagonViewSet, ReceptaViewSet, KalendarzViewSet, KalendarzListView
from django.urls import include, path

router = routers.DefaultRouter()
router.register(r'wizyta', WizytaViewSet)
router.register(r'paragon', ParagonViewSet)
router.register(r'recepta', ReceptaViewSet)
router.register(r'kalendarz', KalendarzViewSet)
app_name = 'wizyta'

urlpatterns = [
    path('api/', include(router.urls)),
    path('api_auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('kalendarz/', KalendarzListView.as_view(), name='kalendarz-list'),
]