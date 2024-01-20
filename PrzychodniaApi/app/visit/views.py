from django.shortcuts import render
from .models import Visit

def user_visits(request):
    user_visits = Visit.objects.filter(patient=request.user.patient)
    return render(request, 'user_visits.html', {'user_visits': user_visits})