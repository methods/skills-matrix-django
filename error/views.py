from django.shortcuts import render


def not_authorised(request):
    return render(request, 'error/not_authorised.html')
