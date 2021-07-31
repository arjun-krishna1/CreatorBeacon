from django.urls import path


from .views import (
    homeView,
    createAccountView,
    loginView,
    qrView,
    creatorDashboardView,
    createEventView,
    createPrizeView,
    enterEventView,
    creatorDashboardEventView
)

urlpatterns = [
    path('', homeView, name='home'),
    path('createAccount/', createAccountView, name='createAccount'),
    path('login/', loginView, name='login'),
    path('qr/<int:event_id>/', qrView, name = "qr"),
    path('creatorDashboard/', creatorDashboardView, name='creatorDashboard'),
    path('createEvent/', createEventView, name='createEvent'),
    path('createPrize/<int:event_id>/', createPrizeView, name='createPrize'),
    path('enterEvent/<int:event_id>/', enterEventView, name='enterEvent'),
    path(
        'creatorDashboardEvent/<int:event_id>/',
        creatorDashboardEventView, name='creatorDashboardEvent'),
]
