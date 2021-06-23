from django.shortcuts import render, redirect
from .forms import NameForm, EmailForm
from django.http import HttpResponseRedirect
from django.urls import reverse


def add_name(request):
    form = NameForm()
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            request.session['first_name'] = request.POST['first_name']
            request.session['surname'] = request.POST['surname']
            request.session.save()
            print(request.session['first_name'])
            print(request.session['surname'])
            return redirect(add_email)
    else:
        form = NameForm()
    return render(request, 'signup/add_name.html', {'form': form})


def add_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            print('valid')
            request.session['email_address'] = request.POST['email_address']
            request.session.save()
            print(request.session['email_address'])
            return redirect(add_job)
        else:
            print('invalid')
            return render(request, 'signup/add_email.html', {'form': form, 'error': True})
    else:
        form = EmailForm()
    return render(request, 'signup/add_email.html', {'form': form})
