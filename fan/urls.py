from django.urls import path

from .views import (
    homeView,
    createAccountView,
    loginView,
    creatorDashboardView,
    createEventView
)

urlpatterns = [
    path('', homeView, name='home'),
    path('createAccount/', createAccountView, name='createAccount'),
    path('login/', loginView, name='login'),
    path('creatorDashboard/', creatorDashboardView, name='creatorDashboard'),
    path('createEvent/', createEventView, name='createEvent'),
]