from django.forms.formsets import formset_factory
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.conf import settings
import qrcodefunctions as q

from .models import Creator, Event, Prize

from .forms import (
    CreateAccountForm,
    LoginForm,
    CreateEventForm,
    CreatePrizeForm
)

def homeView(request):
    context = {"name": "Arjun & Josh"}
    return render(request, "home.html", context)

def createAccountView(request):
    # TODO: only works for admins
    if request.method == 'POST':
        form = CreateAccountForm(request.POST)
        if form.is_valid():
            new_user = User(username = request.POST["email"], password = request.POST["password"])
            new_user.save()
            print(new_user)
            print("account created")
            return render(request, "createAccount_success.html")
        # TODO handle invalid account information
    
    form = CreateAccountForm()
    context = {"form": form}
    return render(request, "createAccount_form.html", context)

def loginView(request):
    context = {}
    if request.method == 'POST':
        print(request.POST['email'])
        user = authenticate(request, username=request.POST['email'], password=request.POST['password'])
        # TODO message about account login success status, you are logged in or please create an account
        if user is not None:
            print("logged in")
            login(request, user)
            return render(request, "login_success.html")
        else:
            print("login failed, try again")


    form = LoginForm()
    context = {"form": form}
    return render(request, "login_form.html", context)

def qrView(request, event_id):
    q.make_website_link_qr(event_id)
    event = Event.objects.get(id=event_id)
    
    context = {}
    context["filename"] = str(event_id)
    context["event_name"] = event.name
    context["creator_name"]= event.creator.user.username
    context["date"]= event.date.strftime("%m/%d/%Y")
    context["start"]= event.start.strftime("%H:%M %p")
    context["end"]= event.end.strftime("%H:%M %p")

    print(context)
    return render(request, "qr.html", context)
  
def creatorDashboardView(request):
    user = request.user
    creator = Creator.objects.filter(user=user)
    print(creator)

    context = {"username": str(user)}
    return render(request, "creator_dashboard.html", context)

def createEventView(request):
    context = {}
    if request.method == 'POST':
        # TODO handle invalid inputs
        creator = Creator.objects.get(user=request.user)
        new_event = Event(
            creator = creator,
            name = request.POST["name"],
            date = request.POST["date"],
            start = request.POST["start"],
            end = request.POST["end"],
        )

        new_event.save()
        print("event created")
        return redirect('createPrize', new_event.id)

    form = CreateEventForm()
    context = {"username": str(request.user), "form": form}
    return render(request, "createEvent.html", context)

form_keys = [
    "form-0-name",
    "form-1-name",
    "form-2-name",
    "form-3-name",
    "form-4-name",
]

def createPrizeView(request, event_id):
    context = {}
    if request.method == 'POST':
        # TODO handle invalid inputs
        print("post data ", request.POST)
        event = Event.objects.get(id=event_id)

        for key in form_keys:
            this_prize = Prize (
                name = request.POST[key],
                event = event,
            )
            this_prize.save()
            
        print("prizes saved")
        return redirect('creatorDashboard')

    PrizeSet = formset_factory(CreatePrizeForm, extra=5)
    form = PrizeSet()
    context = {"username": str(request.user), "form": form}
    return render(request, "createPrize.html", context)
