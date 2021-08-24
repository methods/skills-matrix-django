from django.shortcuts import render, redirect
from .forms import NameForm, JobForm, EmailForm, PasswordForm
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from common.custom_class_view import CustomView
from common.user_group_check_mixins import AdminUserMixin, CustomLoginRequiredMixin


class AddName(CustomView):
    def get(self, request):
        form = NameForm()
        return render(request, 'user_management/name.html', {'form': form})

    def post(self, request):
        form = NameForm(request.POST)
        if form.is_valid():
            form.process_in_signup(request)
            return redirect('add-email')
        return render(request, 'user_management/name.html', {'form': form})


class AddEmail(CustomView):
    def get(self, request):
        form = EmailForm()
        return render(request, 'user_management/email_address.html', {'form': form})

    def post(self, request):
        form = EmailForm(request.POST)
        if form.is_valid():
            form.process_in_signup(request)
            return redirect('add-job')
        return render(request, 'user_management/email_address.html', {'form': form})


class AddJob(CustomView):
    def get(self, request):
        form = JobForm()
        return render(request, 'user_management/job_info.html', {'form': form})

    def post(self, request):
        form = JobForm(request.POST)
        if form.is_valid():
            form.process_in_signup(request)
            return redirect('create-password')
        else:
            self.handle_form_errors(form, request)
            return render(request, 'user_management/job_info.html', {'form': form})


class CreatePassword(CustomView):
    def get(self, request):
        form = PasswordForm()
        return render(request, 'user_management/create_password.html', {'form': form})

    def post(self, request):
        form = PasswordForm(request.POST)
        if form.is_valid():
            form.process(request)
            return redirect('summary')
        return render(request, 'user_management/create_password.html', {'form': form})


class Summary(CustomView):
    def set_user_details(self, request):
        self.first_name = request.session['first_name'] if 'first_name' in request.session else ""
        self.surname = request.session['surname'] if 'surname' in request.session else ""
        self.full_name = f'{self.first_name} {self.surname}'
        self.email_address = request.session['email_address'] if 'email_address' in request.session else ''
        self.team = request.session['team'] if 'team' in request.session else ''
        self.job = request.session['job'] if 'job' in request.session else ''
        self.hashed_password = request.session['hashed_password'] if 'hashed_password' in request.session else ''

    def get(self, request):
        self.set_user_details(request)
        return render(request, 'user_management/summary.html', {'full_name': self.full_name,
                                                                'email_address': self.email_address, 'team': self.team,
                                                                'job': self.job})

    def post(self, request):
        self.set_user_details(request)
        user = get_user_model()
        new_user = user.objects.create_user(self.email_address, self.first_name, self.surname, self.team, self.job,
                                            self.hashed_password)
        group = Group.objects.get(name='Staff')
        new_user.groups.add(group)
        messages.success(request, 'Your registration was successful.')
        return redirect('login')


class EditNameSignup(CustomView):
    def get(self, request):
        first_name = request.session['first_name'] if 'first_name' in request.session else ""
        surname = request.session['surname'] if 'surname' in request.session else ""
        form = NameForm(initial={'first_name': first_name, 'surname': surname})
        return render(request, 'user_management/name.html', {'form': form, 'edit': True})

    def post(self, request):
        if request.method == 'POST':
            form = NameForm(request.POST)
            if form.is_valid():
                form.process_in_signup(request)
                return redirect('summary')


class EditEmailAddressSignup(CustomView):
    def get(self, request):
        form = EmailForm()
        form.fields['email'].initial = request.session[
            'email_address'] if 'email_address' in request.session else ''
        return render(request, 'user_management/email_address.html', {'form': form, 'edit': True})

    def post(self, request):
        form = EmailForm(request.POST)
        if form.is_valid():
            form.process_in_signup(request)
            return redirect('summary')
        return render(request, 'user_management/email_address.html', {'form': form, 'edit': True})


class EditJobInformationSignup(CustomView):
    def get(self, request):
        form = JobForm()
        form.fields['team'].initial = request.session['team'] if 'team' in request.session else ''
        form.fields['job_role'].initial = request.session['job'] if 'job' in request.session else ''
        return render(request, 'user_management/job_info.html', {'form': form, 'edit': True})

    def post(self, request):
        form = JobForm(request.POST)
        if form.is_valid():
            form.process_in_signup(request)
            return redirect('summary')
        return render(request, 'user_management/job_info.html', {'form': form, 'edit': True})


class Profile(CustomLoginRequiredMixin, CustomView):
    def get(self, request):
        return render(request, 'user_management/summary.html', {"user_details": request.user})


class EditName(CustomLoginRequiredMixin, CustomView):
    def get(self, request):
        first_name = request.user.first_name if request.user.first_name else ""
        surname = request.user.surname if request.user.surname else ""
        form = NameForm(initial={'first_name': first_name, 'surname': surname})
        return render(request, 'user_management/name.html', {'form': form, 'edit_profile': True})

    def post(self, request):
        form = NameForm(request.POST)
        if form.is_valid():
            request.user.update_from_request(form.cleaned_data)
            return redirect('profile')
        return render(request, 'user_management/name.html', {'form': form, 'edit_profile': True})


class EditEmail(CustomLoginRequiredMixin, CustomView):
    def get(self, request):
        email_address = request.user.email
        form = EmailForm(initial={'email': email_address})
        return render(request, 'user_management/email_address.html', {'form': form, 'edit_profile': True})

    def post(self, request):
        form = EmailForm(request.POST)
        if form.is_valid():
            request.user.update_from_request(form.cleaned_data)
            return redirect('profile')
        return render(request, 'user_management/email_address.html', {'form': form, 'edit_profile': True})


class EditJobInformation(CustomLoginRequiredMixin, CustomView):
    def get(self, request):
        job = request.user.job_role
        team = request.user.team
        form = JobForm(initial={'team': team, 'job_role': job})
        return render(request, 'user_management/job_info.html', {'form': form, 'edit_profile': True})

    def post(self, request):
        form = JobForm(request.POST)
        if form.is_valid():
            request.user.update_from_request(form.cleaned_data)
            return redirect('profile')
        return render(request, 'user_management/job_info.html', {'form': form, 'edit_profile': True})
