from django.shortcuts import render, redirect
from .forms import NameForm


def add_name(request):
    # if this is a POST request we need to process the form data
    form = NameForm()
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            request.session['first_name'] = request.POST['first_name']
            request.session['surname'] = request.POST['surname']
            request.session.save()
            return redirect('email/')
    else:
        form = NameForm()

    return render(request, 'signup/add_name.html', {'form': form})


def add_email(request):
    return render(request, 'signup/add_email.html')


def add_job(request):
    return render(request, 'signup/add_job.html')
