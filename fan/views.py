from django.forms.formsets import formset_factory
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.conf import settings

from datetime import datetime

import qrcodefunctions as q

from .models import (
    Creator,
    Event,
    Prize,
    Entry,
    Fan,
)

from .forms import (
    CreateAccountForm,
    LoginForm,
    CreateEventForm,
    CreatePrizeForm
)

def homeView(request):
    name = "Log in!"

    if request.user:
        name = request.user.username

    context = {"name": name}
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

form_keys = (
    "form-0-name",
    "form-1-name",
    "form-2-name",
    "form-3-name",
    "form-4-name",
)

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

def get_diff_time(a, b):
    zero_day = datetime.now()
    start = datetime.combine(zero_day.date(), a)
    end = datetime.combine(zero_day.date(), b)
    return zero_day + (end - start )

def enterEventView(request, event_id):
    event = Event.objects.get(id=event_id)
    curr_time = datetime.now().time()

    
    fan = Fan.objects.filter(user=request.user)

    if len(fan) == 0:
        fan = Fan(user = request.user)
        fan.save()

    else:
        fan = fan[0]

    context = {}

    come_back_at = event.end.strftime("%H:%M %p")
    event_status = event.getStatus()
    if event_status == event.status_choices["not_started"]:
        context["time_left"] = get_diff_time(event.start, curr_time).strftime("%H:%M:%S")
        start_time_str = event.start.strftime("%H:%M %p")
        context["status"] = f"Come back at { start_time_str } to enter"

    elif event_status == event.status_choices["in_progress"]:
        fan.enter(event_id)
        end_time_str = event.start.strftime("%H:%M %p")
        context["time_left"] = get_diff_time(event.end, curr_time).strftime("%H:%M:%S")
        context["status"] = f"You are entered! Come back after { come_back_at } to see if you won"
    
    else:
        # redirect to page where it shows winners, show if they won
        context["time_left"] = "00:00:00"

        entry = Entry.objects.get(event=event, fan=fan)

        if entry and entry.won:
            context["status"] = f"Congratulations! you won a { entry.prize.name }"

        else:
            context["status"] = f"😔 you didn't win this time..."

    return render(request, "countdown.html", context)

def creatorDashboardEventView(request, event_id):
    print(event_id)
    print(type(event_id))
    event = Event.objects.filter(event_id)
    print(event)
    event = event[0]
    winningEntries = Entry.objects.filter(won=True)

    if not(len(winningEntries)):
        winningEntries = event.chooseWinners()

    winningFans = ( (entry.fan, entry.prize) for entry in winningEntries)
    
    losingEntries = Entry.objects.filter(won=False)
    losingFans = (entry.fan for entry in losingEntries)

    context = {"winningFans": winningFans, "losingFans": losingFans}
    print(context)

    return render(request, "creatorDashboardEvent.html", context)

