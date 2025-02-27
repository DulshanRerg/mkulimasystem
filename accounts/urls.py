from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    # Registration view
    path('signup/', views.SignUpView.as_view(), name='signup'),
    
    # Login view (using Django's built-in authentication)
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    
    # Logout view
    path('logout/', auth_views.LogoutView.as_view(next_page='accounts:login'), name='logout'),
    
    # Profile view (you can expand this later)
    path('profile/', views.ProfileView.as_view(), name='profile'),
]
