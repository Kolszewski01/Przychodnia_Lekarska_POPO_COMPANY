from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from user.forms import CustomAuthenticationForm
# from PRZYCHODNIAPSI.app.app.forms import CustomLoginForm


def home(request):
    return render(request, 'index.html')



class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'registration/login.html'

    def form_valid(self, form):
        """Zastosuj logikę po poprawnym zalogowaniu."""
        response = super().form_valid(form)
        # Dodaj dodatkową logikę, jeśli jest taka potrzeba
        return response


