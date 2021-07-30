from django.shortcuts import render

def homeView(request):
    context = {"name": "Arjun & Josh"}
    return render(request, "home.html", context)
