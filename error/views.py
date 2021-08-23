from django.shortcuts import render, redirect, reverse
from common.custom_class_view import CustomView


class Unauthorised(CustomView):
    def get(self, request):
        return redirect(reverse('login-unauthorised'))


class Forbidden(CustomView):
    def get(self, request):
        return render(request, 'error/forbidden.html')