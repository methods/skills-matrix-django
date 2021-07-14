from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def browse_career_paths(request):
    return render(request, 'career_paths/browse_career_paths.html')
