from django.urls import path


from .views import (
    homeView,
    createAccountView,
    loginView,
    qrView,
    creatorDashboardView,
)

urlpatterns = [
    path('', homeView, name='home'),
    path('createAccount/', createAccountView, name='createAccount'),
    path('login/', loginView, name='login'),
    path('<int:id>/qr/', qrView, name = "qr"),
    path('creatorDashboard/', creatorDashboardView, name='creatorDashboard'),
]