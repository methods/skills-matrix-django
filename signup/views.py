from django.shortcuts import render, redirect
from .forms import NameForm, JobForm, EmailForm, PasswordForm
import hashlib
from django.contrib.auth import get_user_model


def add_name(request):
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
            request.session['hashed_password'] = hashed_password
            request.session.save()
            return render(request, 'signup/create_password.html')
        else:
            render(request, 'signup/create_password.html', {'form': form})
    else:
        form = PasswordForm()
    return render(request, 'signup/create_password.html', {'form': form})
  

def summary(request):
    first_name = request.session['first_name'] if 'first_name' in request.session else ""
    surname = request.session['surname'] if 'surname' in request.session else ""
    full_name = f'{first_name} {surname}'
    email_address = request.session['email_address'] if 'email_address' in request.session else ''
    team = request.session['team'] if 'team' in request.session else ''
    job = request.session['job'] if 'job' in request.session else ''
    if request.method == 'POST':
        user = get_user_model()
        user.objects.create_user(email_address, first_name, surname, team, job)
        return redirect('/')
    return render(request, 'signup/summary.html', {'full_name': full_name, 'email_address': email_address,
                                                   'team': team, 'job': job})


def edit_name(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            request.session['first_name'] = request.POST['first_name']
            request.session['surname'] = request.POST['surname']
            request.session.save()
            return redirect(summary)
    else:
        first_name = request.session['first_name'] if 'first_name' in request.session else ""
        surname = request.session['surname'] if 'surname' in request.session else ""
        form = NameForm(initial={'first_name': first_name, 'surname': surname})
    return render(request, 'signup/add_name.html', {'form': form, 'edit': True})


def edit_email_address(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            request.session['email_address'] = request.POST['email_address']
            request.session.save()
            return redirect(summary)
    else:
        form = EmailForm()
        form.fields['email_address'].initial = request.session[
            'email_address'] if 'email_address' in request.session else ''
    return render(request, 'signup/add_email.html', {'form': form, 'edit': True})


def edit_job_information(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            request.session['team'] = request.POST['team']
            request.session['job'] = request.POST['job']
            request.session.save()
            return redirect(summary)
    else:
        form = JobForm()
        form.fields['team'].initial = request.session['team'] if 'team' in request.session else ''
        form.fields['job'].initial = request.session['job'] if 'job' in request.session else ''
    return render(request, 'signup/add_job.html', {'form': form, 'edit': True})
