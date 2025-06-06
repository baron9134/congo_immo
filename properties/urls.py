from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.home, name='home'),
    path('property/<int:pk>/', views.property_detail, name='property_detail'),
    path('add/', views.add_property, name='add_property'),
    path('mes-biens/', views.my_properties, name='my_properties'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('modifier-bien/<int:pk>/', views.edit_property, name='edit_property'),
]
