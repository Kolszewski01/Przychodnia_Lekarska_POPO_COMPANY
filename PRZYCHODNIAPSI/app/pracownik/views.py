from django.shortcuts import render
from rest_framework import viewsets
from .models import Lekarz, Pracownik
from .serializers import PracownikSerializer, LekarzSerializer

# Create your views here.
class PracownikViewSet(viewsets.ModelViewSet):
    queryset = Pracownik.objects.all()
    serializer_class = PracownikSerializer


class LekarzViewSet(viewsets.ModelViewSet):
    queryset = Lekarz.objects.all()
    serializer_class = LekarzSerializer

