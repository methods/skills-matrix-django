from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    db = get_user_model()
    all_users = db.objects.all()
    context = {"users": all_users}
    return render(request, "app/dashboard.html", context)


@login_required
def edit_skills(request):
    return render(request, "app/edit_skills.html")


@login_required
def browse_profiles(request):
    return render(request, 'app/browse_profiles.html')
