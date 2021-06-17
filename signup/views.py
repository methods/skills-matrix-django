from django.shortcuts import render

# Create your views here.


def add_name(request):
    return render(request, "signup/add_name.html")
