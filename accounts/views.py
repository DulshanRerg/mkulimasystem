from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from .forms import CustomUserCreationForm, CustomUserUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

class SignUpView(generic.CreateView):
    """
    Handles user registration using the CustomUserCreationForm.
    """
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:login')

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

@login_required
def profile_view(request):
    """
    Displays and updates user profile.
    """
    user = request.user  #  Get the logged-in user
    user_role = user.role  #  Determine the user role

    if request.method == "POST":
        form = CustomUserUpdateForm(request.POST, request.FILES, instance=user, user_role=user_role)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')  #  Ensure page refreshes after update
    else:
        form = CustomUserUpdateForm(instance=user, user_role=user_role)

    return render(request, 'accounts/profile_update.html', {'form': form, 'user': user, 'user_role': user_role})
