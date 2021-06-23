from django.shortcuts import render, redirect
from .forms import NameForm


def add_name(request):
    form = NameForm()
    if request.method == 'POST':
        form = NameForm(request.POST)
        # breakpoint()
        if form.is_valid():
            request.session['first_name'] = request.POST['first_name']
            request.session['surname'] = request.POST['surname']
            request.session.save()
            print(request.session['first_name'])
            print(request.session['surname'])
            return redirect('email/')
    else:
        form = NameForm()
    return render(request, 'signup/add_name.html', {'form': form})


def add_email(request):
    return render(request, 'signup/add_email.html')
