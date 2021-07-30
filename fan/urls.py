from django.urls import path


from .views import (
    homeView,
    createAccountView,
    loginView,
    qrView
)

urlpatterns = [
    path('', homeView, name='home'),
    path('createAccount/', createAccountView, name='createAccount'),
    path('login/', loginView, name='login'),
    path('qr/', qrView, name = "qr")
]