from django.urls import path
from django.contrib.auth import views as auth_views
from .views import SignUpView, ProfileView, custom_logout_view, register, profile_view, user_profile

app_name = 'accounts'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', profile_view, name='profile_edit'),
    path('profile/<str:username>/', user_profile, name='user_profile'),
    path('logout/', custom_logout_view, name='logout'),
    path('register/', register, name='register'),
]
