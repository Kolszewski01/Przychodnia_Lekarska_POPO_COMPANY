from django.shortcuts import render
from .models import Dokumentacja_medyczna
from .serializers import Dokumentacja_medycznaSerializer
from rest_framework import viewsets
from django.shortcuts import render


# Create your views here.

class Dokumentacja_medycznaViewSet(viewsets.ModelViewSet):
    queryset = Dokumentacja_medyczna.objects.all()
    serializer_class = Dokumentacja_medycznaSerializer

def index(request):
    return render(request, 'index.html')