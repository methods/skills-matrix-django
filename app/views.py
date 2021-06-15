from django.shortcuts import render


def index(request): #the index view
    return render(request, "app/home.html")
