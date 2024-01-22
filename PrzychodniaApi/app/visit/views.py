from django.contrib import messages
from django.shortcuts import render
from django.views import View
from .forms import VisitForm
from .models import Visit


def user_visits(request):
    user_visits = Visit.objects.filter(patient=request.user.patient)
    return render(request, 'user_visits.html', {'user_visits': user_visits})


class VisitCreateView(View):
    template_name = 'add_visit.html'

    def get(self, request, *args, **kwargs):
        form = VisitForm()
        return render(request, self.template_name, {'form': form, 'success_message': None})

    def post(self, request, *args, **kwargs):
        form = VisitForm(request.POST)

        if form.is_valid():
            visit = form.save(commit=False)
            visit.save()

            success_message = 'Pomyślnie zapisano na wizytę!'
            messages.success(request, success_message)
            return render(request, self.template_name, {'form': VisitForm(), 'success_message': success_message})

        return render(request, self.template_name, {'form': form, 'success_message': None})