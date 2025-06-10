from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import cgu_view, activate


urlpatterns = [
    path('', views.home, name='home'),
    path('property/<int:pk>/', views.property_detail, name='property_detail'),
    path('add/', views.add_property, name='add_property'),
    path('mes-biens/', views.my_properties, name='my_properties'),
    path('login/', auth_views.LoginView.as_view(template_name='properties/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('modifier-bien/<int:pk>/', views.edit_property, name='edit_property'),
    path('signup/', views.signup_view, name='signup'),
    path('cgu/', cgu_view, name='cgu'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile_view'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('profile/change-password/', auth_views.PasswordChangeView.as_view(
        template_name='profile/change_password.html',
        success_url='/profile/'
    ),  name='change_password'),
    path('modifier-bien/<int:pk>/', views.edit_property, name='edit_property'),
    path('supprimer-bien/<int:pk>/', views.delete_property, name='delete_property'),
    path('verification-email/', views.email_verification_notice, name='email_verification_notice'),
    path('resend-activation/', views.resend_activation, name='resend_activation'),
    path('property/<int:pk>/', views.property_detail, name='property_detail'),
    path('property/<int:pk>/like/', views.toggle_like, name='toggle_like'),
]

