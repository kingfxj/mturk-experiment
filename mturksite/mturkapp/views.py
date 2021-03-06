from .forms import assignmentForm
from .models import Assignments
from django.contrib import messages
from django.shortcuts import HttpResponse, redirect, render


# Create your views here.
def assignmentView(request):
    all_items = Assignments.objects.all()
    if request.method == "POST":
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        birthYear = request.POST.get('birthYear')
        birthCity = request.POST.get('birthCity')
        if name != '' and name is not None:
            all_items = all_items.filter(name__icontains=name)
        if surname != '' and surname is not None:
            all_items = all_items.filter(surname__icontains=surname)
        if birthYear != '' and birthYear is not None:
            all_items = all_items.filter(birthYear__icontains=birthYear)
        if birthCity != '' and birthCity is not None:
            all_items = all_items.filter(birthCity__icontains=birthCity)
    return render(request, 'assignment.html', {"all_items": all_items})


def addAssignment(request):
    if request.method == "POST":
        form = assignmentForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Item has been added!")
            return redirect(assignmentView)
        else:
            messages.success(request, "Item was not added")
            return redirect(assignmentView)
    else:
        all_items = Assignments.objects.all()
        return render(request, 'addAssignment.html', {"all_items": all_items})


def editAssignment(request, list_id):
    if request.method == "POST":
        item = Assignments.objects.get(pk=list_id)
        try:
            form = assignmentForm(request.POST or None, instance=item)
        except ValueError:
            return redirect(assignmentView)
        else:
            if form.is_valid():
                form.save()
                messages.success(request, "Item has been edited!")
                return redirect(assignmentView)
            else:
                return redirect(assignmentView)
    else:
        item = Assignments.objects.get(pk=list_id)
        return render(request, 'editAssignment.html', {"item": item})


def deleteAssignment(request, list_id):
    item = Assignments.objects.get(pk=list_id)
    item.delete()
    messages.success(request, "Item has been deleted from the list!")
    return redirect(assignmentView)


def maintenanceView(request):
    all_items = Assignments.objects.all()
    return render(request, 'maintenance.html', {"all_items": all_items})


def userManagementView(request):
    all_items = Assignments.objects.all()
    return render(request, 'management.html', {"all_items": all_items})


def lobbyView(request):
    all_items = Assignments.objects.all()
    return render(request, 'lobby.html', {"all_items": all_items})


def hitView(request):
    all_items = Assignments.objects.all()
    return render(request, 'hit.html', {"all_items": all_items})
