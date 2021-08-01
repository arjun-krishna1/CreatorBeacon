from django.forms.formsets import formset_factory
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages

import datetime

import qrcodefunctions as q

from .models import (
    Creator,
    Event,
    Prize,
    Entry,
    Fan,
)


def split_time_string(time_string):
    output = {
        "hour": time_string[:2],
        "minute": time_string[2:4],
        "second": time_string[4:6],
    }
    return output

def get_diff_time2(chosen_time): #takes in format hhmmss
    chosen_time = split_time_string(chosen_time)
    current = split_time_string(datetime.datetime.now().strftime("%H%M%S"))
    diff = lambda x: "{:02d}".format(abs(int(chosen_time.get(x, 0)) - int(current.get(x, 0))))
    difference = [diff("hour"), diff("minute"), diff("second")]
    return ":".join(difference)


def get_diff_time(a):
    value = get_diff_time2(str(a).replace(":", ""))
    return value

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
            new_user = User(username = request.POST["username"], password = request.POST["password"])
            new_user.save()
            #print(new_user)
            #print("account created")
            return render(request, "createAccount_success.html")
        # TODO handle invalid account information
    
    form = CreateAccountForm()
    context = {"form": form}
    return render(request, "createAccount_form.html", context)

def loginView(request):
    context = {}
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        # TODO message about account login success status, you are logged in or please create an account
        if user is not None:
            #print("logged in")
            login(request, user)
            messages.add_message(request, messages.SUCCESS, 'Logged in!')
            return redirect("creatorDashboard")
        else:
            messages.add_message(request, messages.ERROR, '😔 Login Failed')
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

    #print(context)
    return render(request, "qr.html", context)
  
def creatorDashboardView(request):
    user = request.user
    creator = Creator.objects.get(user=user)

    event_objects = Event.objects.filter(creator=creator)

    finished_events = []
    events = []
    for event in event_objects:
        if event.getStatus() == Event.status_choices["over"]:
            finished_events.append(event)
        else:
            events.append(event)

    context = {"username": str(user), "events": events, "finished_events": finished_events,  "profile_path": creator.img.url}
    print(context)
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
        #print("event created")
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
        #print("post data ", request.POST)
        event = Event.objects.get(id=event_id)

        for key in form_keys:
            this_prize = Prize (
                name = request.POST[key],
                event = event,
            )
            this_prize.save()
            
        #print("prizes saved")
        return redirect('creatorDashboard')

    PrizeSet = formset_factory(CreatePrizeForm, extra=5)
    form = PrizeSet()
    context = {"username": str(request.user), "form": form}
    return render(request, "createPrize.html", context)




def enterEventView(request, event_id):
    event = Event.objects.get(id=event_id)

    fan = Fan.objects.filter(user=request.user)

    if len(fan) == 0:
        fan = Fan(user = request.user)
        fan.save()

    else:
        fan = fan[0]

    context = {"profile_path": event.creator.img.url, "event": event }

    come_back_at = event.end.strftime("%H:%M %p")
    event_status = event.getStatus()
    if event_status == event.status_choices["not_started"]:
        context["time_left"] = get_diff_time(event.start)
        start_time_str = event.start.strftime("%H:%M %p")
        context["status"] = f"Come back at { start_time_str } to enter"

    elif event_status == event.status_choices["in_progress"]:
        fan.enter(event_id)
        end_time_str = event.start.strftime("%H:%M %p")
        context["time_left"] = get_diff_time(event.end)
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
    event = Event.objects.get(id=event_id)

    context = {"event": event, "event_over": event.getStatus()==Event.status_choices["over"]}

    entries = Entry.objects.filter(event=event)
    context["entries"] = entries

    if event.getStatus() == Event.status_choices["over"]:
        winning_entries = entries.filter(won=True)

        if not(len(winning_entries)):
            event.chooseWinners()
            winning_entries = entries.filter(won=True)

        context["winning_entries"] = winning_entries

    return render(request, "creatorDashboardEvent.html", context)

