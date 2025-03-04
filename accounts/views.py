from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from .forms import CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

class SignUpView(generic.CreateView):
    """
    Handles user registration using the CustomUserCreationForm.
    """
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:profile')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

class ProfileView(LoginRequiredMixin, TemplateView):
    """
    Displays the user profile.
    """
    template_name = 'accounts/profile.html'

def custom_logout_view(request):
    """
    Custom logout view that allows GET requests.
    """
    logout(request)
    return redirect(reverse_lazy('accounts:login'))

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('accounts:profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})  # Update to use signup.html
