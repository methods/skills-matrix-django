from django.shortcuts import render


def index(request):
    return render(request, "app/home.html")


def edit_skills(request):
    return render(request, "app/edit_skills.html")
