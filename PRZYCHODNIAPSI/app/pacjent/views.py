from django.shortcuts import render
from rest_framework import viewsets
from .models import Pacjent
from .serializers import PacjentSerializer


class PacjentViewSet(viewsets.ModelViewSet):
    queryset = Pacjent.objects.all()
    serializer_class = PacjentSerializer
