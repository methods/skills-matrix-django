from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required


@login_required
def profile(request):
    return render(request, 'user_profile/profile.html', {"user": request.user})
