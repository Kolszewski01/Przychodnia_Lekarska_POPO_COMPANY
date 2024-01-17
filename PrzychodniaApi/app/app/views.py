from django.shortcuts import render


def home(request):
    role = getattr(request.user, 'role', None) if request.user.is_authenticated else None
    return render(request, 'index.html', {'role': role})


