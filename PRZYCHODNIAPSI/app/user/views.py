from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views import View

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'  # Szablon, do którego zostanie przekierowany użytkownik po zalogowaniu
    form_class = CustomAuthenticationForm
    success_url = reverse_lazy('home')

    def register_view(request):
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                return redirect('home')
        else:
            form = CustomUserCreationForm()

        return render(request, 'register.html', {'form': form})

class CustomLogoutView(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')  # Zmiana na odpowiednią ścieżkę
