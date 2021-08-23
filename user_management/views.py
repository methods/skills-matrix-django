from django.shortcuts import render, redirect
from .forms import NameForm, JobForm, EmailForm, PasswordForm
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from common.custom_class_view import CustomView


class AddName(CustomView):
    def get(self, request):
        form = NameForm()
        return render(request, 'user_management/name.html', {'form': form})

    def post(self, request):
        form = NameForm(request.POST)
        if form.is_valid():
            request.session['first_name'] = request.POST['first_name']
            request.session['surname'] = request.POST['surname']
            request.session.save()
            return redirect(add_email)
        return render(request, 'user_management/name.html', {'form': form})


def add_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            request.session['email_address'] = request.POST['email_address']
            request.session.save()
            return redirect(add_job)
    else:
        form = EmailForm()
    return render(request, 'user_management/email_address.html', {'form': form})


def add_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            request.session['team'] = request.POST['team']
            request.session['job'] = request.POST['job']
            request.session.save()
            return redirect(create_password)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = JobForm()
    return render(request, 'user_management/job_info.html', {'form': form})


def create_password(request):
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            password = request.POST['password']
            hashed_password = make_password(password)
            request.session['hashed_password'] = hashed_password
            request.session.save()
            return redirect(summary)
    else:
        form = PasswordForm()
    return render(request, 'user_management/create_password.html', {'form': form})


def summary(request):
    first_name = request.session['first_name'] if 'first_name' in request.session else ""
    surname = request.session['surname'] if 'surname' in request.session else ""
    full_name = f'{first_name} {surname}'
    email_address = request.session['email_address'] if 'email_address' in request.session else ''
    team = request.session['team'] if 'team' in request.session else ''
    job = request.session['job'] if 'job' in request.session else ''
    hashed_password = request.session['hashed_password'] if 'hashed_password' in request.session else ''
    if request.method == 'POST':
        user = get_user_model()
        new_user = user.objects.create_user(email_address, first_name, surname, team, job, hashed_password)
        group = Group.objects.get(name='Staff')
        new_user.groups.add(group)
        messages.success(request, 'Your registration was successful.')
        return redirect('login') 
    return render(request, 'user_management/summary.html', {'full_name': full_name, 'email_address': email_address,
                                                   'team': team, 'job': job})


def edit_name_signup(request):
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
        return render(request, 'user_management/name.html', {'form': form, 'edit': True})


def edit_email_address_signup(request):
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
    return render(request, 'user_management/email_address.html', {'form': form, 'edit': True})


def edit_job_information_signup(request):
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
    return render(request, 'user_management/job_info.html', {'form': form, 'edit': True})


@login_required
def profile(request):
    return render(request, 'user_management/summary.html', {"user_details": request.user})


@login_required
def edit_name(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            request.user.first_name = request.POST['first_name']
            request.user.surname = request.POST['surname']
            request.user.save()
            return redirect(profile)
    else:
        first_name = request.user.first_name if request.user.first_name else ""
        surname = request.user.surname if request.user.surname else ""
        form = NameForm(initial={'first_name': first_name, 'surname': surname})
        return render(request, 'user_management/name.html', {'form': form, 'edit_profile': True})


@login_required
def edit_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            request.user.email = request.POST['email_address']
            request.user.save()
            return redirect(profile)
    else:
        email_address = request.user.email
        form = EmailForm(initial={'email_address': email_address})
        return render(request, 'user_management/email_address.html', {'form': form, 'edit_profile': True})


@login_required
def edit_job_information(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            request.user.team = request.POST['team']
            request.user.job_role = request.POST['job']
            request.user.save()
            return redirect(profile)
    else:
        job = request.user.job_role
        team = request.user.team
        form = JobForm(initial={'team': team, 'job': job})
    return render(request, 'user_management/job_info.html', {'form': form, 'edit_profile': True})
