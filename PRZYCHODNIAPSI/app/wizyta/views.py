from django.shortcuts import render
from django.views.generic import ListView

from .models import Wizyta, Paragon, Recepta, Kalendarz
from rest_framework import viewsets
from .serializers import ReceptaSerializer, WizytaSerializer, ParagonSerializer, KalendarzSerializer

# Create your views here.
class WizytaViewSet(viewsets.ModelViewSet):
    queryset = Wizyta.objects.all()
    serializer_class = WizytaSerializer


class ParagonViewSet(viewsets.ModelViewSet):
    queryset = Paragon.objects.all()
    serializer_class = ParagonSerializer

class ReceptaViewSet(viewsets.ModelViewSet):
    queryset = Recepta.objects.all()
    serializer_class = ReceptaSerializer

class KalendarzViewSet(viewsets.ModelViewSet):
    queryset = Kalendarz.objects.all()
    serializer_class = KalendarzSerializer

class KalendarzListView(ListView):
    model = Kalendarz
    template_name = 'kalendarz_list.html'  # Utwórz szablon HTML, w którym będą wyświetlane dane
    context_object_name = 'kalendarz_list'
