from django.shortcuts import render
from django.contrib.auth import get_user_model


def index(request):
    db = get_user_model()
    all_users = db.objects.all()
    context = {"users": all_users}
    return render(request, "app/home.html", context)


def edit_skills(request):
    return render(request, "app/edit_skills.html")
