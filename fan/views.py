from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

def homeView(request):
    context = {"name": "Arjun & Josh"}
    return render(request, "home.html", context)

def createAccountView(request):
    context = {}
    if request.method == 'POST':
        new_user = User(username = request.POST["username"], password = request.POST["password"])
        new_user.save()
        print("account created")
        return render(request, "createAccount_success.html")

    return render(request, "createAccount_form.html", context)

def loginView(request):

    context = {}
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        # TODO message about account login success status, you are logged in or please create an account
        if user is not None:
            print("logged in")
            login(request, user)
            return render(request, "login_success.html", context)
        else:
            print("login failed, try again")
        
    return render(request, "login_form.html", context)
