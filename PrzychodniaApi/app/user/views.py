from django.contrib.auth import logout
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from rest_framework import generics, authentication, permissions, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from django.shortcuts import render, redirect
from user.serializers import UserSerializer, AuthTokenSerializer
from .forms import CustomLoginForm


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""

    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""

    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""

    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self):
        """Retrieve and return authenticated user"""

        return self.request.user


class CustomLogoutView(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')


class CustomLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = CustomLoginForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')
        if not remember_me:
            self.request.session.set_expiry(0)
        return super().form_valid(form)
