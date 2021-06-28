from django.shortcuts import render, redirect
from .forms import NameForm, JobForm, EmailForm, PasswordForm
import hashlib



def add_name(request):
    form = NameForm()
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            request.session['first_name'] = request.POST['first_name']
            request.session['surname'] = request.POST['surname']
            request.session.save()
            return redirect(add_email)
    else:
        form = NameForm()
    return render(request, 'signup/add_name.html', {'form': form})


def add_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            request.session['email_address'] = request.POST['email_address']
            request.session.save()
            return redirect(add_job)
        else:
            return render(request, 'signup/add_email.html', {'form': form, 'error': True})
    else:
        form = EmailForm()
    return render(request, 'signup/add_email.html', {'form': form})


def add_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            request.session['team'] = request.POST['team']
            request.session['job'] = request.POST['job']
            request.session.save()
            return redirect(create_password)
    else:
        form = JobForm()
    return render(request, 'signup/add_job.html', {'form': form})


def create_password(request):
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            password = request.POST['password']
            hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
            request.session['password'] = hashed_password
            request.session.save()
            return redirect(check_your_details)
        else:
            render(request, 'signup/create_password.html', {'form': form})
    else:
        form = PasswordForm()
    return render(request, 'signup/create_password.html', {'form': form})



