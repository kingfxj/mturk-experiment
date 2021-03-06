from .forms import assignmentForm, SignUpForm
from .models import Assignment
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


# Create your views here.
@login_required
def login(request):
    return render(request, 'assignment.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password, is_superuser=True, is_staff=True)
            login(request, user)
            return redirect('assignmentView')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def homeView(request):
    return render(request, 'home.html')


def assignmentView(request):
    all_items = Assignment.objects.all()
    if request.method == "POST":
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        birthYear = request.POST.get('birthYear')
        birthCity = request.POST.get('birthCity')
        active = request.POST.get('active')
        if name != '' and name is not None:
            all_items = all_items.filter(name__icontains=name)
        if surname != '' and surname is not None:
            all_items = all_items.filter(surname__icontains=surname)
        if birthYear != '' and birthYear is not None:
            all_items = all_items.filter(birthYear__icontains=birthYear)
        if birthCity != '' and birthCity is not None:
            all_items = all_items.filter(birthCity__icontains=birthCity)
        if active != '' and active is not None:
            all_items = all_items.filter(active__icontains=active)
    return render(request, 'assignment.html', {"all_items": all_items})


def addAssignment(request):
    if request.method == "POST":
        form = assignmentForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Item has been added!")
            return redirect(assignmentView)
        else:
            print(form.errors)
            messages.error(request, "Item was not added")
            return redirect(assignmentView)
    else:
        all_items = Assignment.objects.all()
        return render(request, 'addAssignment.html', {"all_items": all_items})


def editAssignment(request, list_id):
    if request.method == "POST":
        item = Assignment.objects.get(pk=list_id)
        try:
            form = assignmentForm(request.POST or None, instance=item)
        except ValueError:
            print(form.errors)
            messages.error(request, "Item was not edited")
            return redirect(assignmentView)
        else:
            if form.is_valid():
                form.save()
                messages.success(request, "Item has been edited!")
                return redirect(assignmentView)
            else:
                print(form.errors)
                print(form.data)
                messages.error(request, "Item was not edited")
                return redirect(assignmentView)
    else:
        item = Assignment.objects.get(pk=list_id)
        return render(request, 'editAssignment.html', {"item": item})


def deleteAssignment(request, list_id):
    item = Assignment.objects.get(pk=list_id)
    item.delete()
    messages.success(request, "Item has been deleted from the list!")
    return redirect(assignmentView)


def qualificationView(request):
    all_items = Assignment.objects.all()
    return render(request, 'qualification.html', {"all_items": all_items})


def lobbyView(request):
    all_items = Assignment.objects.all()
    return render(request, 'lobby.html', {"all_items": all_items})


def hitView(request):
    all_items = Assignment.objects.all()
    return render(request, 'hit.html', {"all_items": all_items})
