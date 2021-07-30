from django.urls import path

from .views import (
    homeView,
    createAccountView,
    loginView,
    creatorDashboardView
)

urlpatterns = [
    path('', homeView, name='home'),
    path('createAccount/', createAccountView, name='createAccount'),
    path('login/', loginView, name='login'),
    path('creatorDashboard/', creatorDashboardView, name='creatorDashboard'),
]