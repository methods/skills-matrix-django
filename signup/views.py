from django.shortcuts import render, redirect
from .forms import NameForm

# Create your views here.


def add_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            request.session['first_name'] = request.POST['first_name']
            request.session['surname'] = request.POST['surname']
            request.session.save()
            print(request.session['first_name'])
            print(request.session['surname'])
            return redirect(request.path)
    else:
        form = NameForm()

    return render(request, 'add_name.html', {'form': form})
