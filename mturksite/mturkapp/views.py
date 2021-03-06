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
    """
    Home View
    :param request
    :return: Home page
    """
    return render(request, 'home.html')


def assignmentView(request):
    """
    View Assignment
    :param request
    :return: Assignment page
    """
    all_items = Assignment.objects.all()
    if request.method == "POST":
        name = request.POST.get('name')             # Retrieve query for name
        surname = request.POST.get('surname')       # Retrieve query for surname
        birthYear = request.POST.get('birthYear')   # Retrieve query for Birth Year
        birthCity = request.POST.get('birthCity')   # Retrieve query for Birth City
        active = request.POST.get('active')         # Retrieve query for active
        # Filter the objects according to the sort
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
    # Return the objects that satisfy all search filter
    return render(request, 'assignment.html', {"all_items": all_items})


def addAssignment(request):
    """
    Add a new assignment
    :param request
    :return: Redirect to Assignment View page after changes are made
    """
    if request.method == "POST":
        form = assignmentForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Item has been added!")
            return redirect(assignmentView)
        else:
            messages.error(request, "Item was not added")
            return redirect(assignmentView)
    else:
        all_items = Assignment.objects.all()
        return render(request, 'addAssignment.html', {"all_items": all_items})


def editAssignment(request, list_id):
    """
    Edit the values of the specific assignments, leave values the same if they are unchanged
    :param request
    :param list_id: The ID of the assignments that needs to be changed
    :return: Return to Assignment View page after changes are made
    """
    if request.method == "POST":
        item = Assignment.objects.get(pk=list_id)   # Retrieve the data to edit
        active = item.active                        # Save original value for active
        try:
            form = assignmentForm(request.POST or None, instance=item)
        except ValueError:
            messages.error(request, "Item was not edited")
            return redirect(assignmentView)
        else:
            if form.is_valid():
                form.save()
                # If data for active is not changed, change it back to original value
                if form.data['active'] == '':
                    newItem = Assignment.objects.get(pk=list_id)
                    newItem.active = active         # Change back the value for active
                    newItem.save()                  # Save the change
                messages.success(request, "Item has been edited!")
                return redirect(assignmentView)
            else:
                messages.error(request, "Item was not edited")
                return redirect(assignmentView)
    else:
        # Edit the specific item
        item = Assignment.objects.get(pk=list_id)
        return render(request, 'editAssignment.html', {"item": item})


def deleteAssignment(request, list_id):
    """
    Delete a specific assignment
    :param request
    :param list_id: The ID of the assignments that needs to be deleted
    :return: Return to Assignment View page after deletion
    """
    item = Assignment.objects.get(pk=list_id)
    item.delete()
    messages.success(request, "Item has been deleted from the list!")
    return redirect(assignmentView)


def qualificationView(request):
    """
    Qualification View Page
    :param request
    :return: Qualification view page
    """
    all_items = Assignment.objects.all()
    return render(request, 'qualification.html', {"all_items": all_items})


def lobbyView(request):
    """
    Lobby View Page
    :param request
    :return: Lobby view page
    """
    all_items = Assignment.objects.all()
    return render(request, 'lobby.html', {"all_items": all_items})


def hitView(request):
    """
    Hit View Page
    :param request
    :return: Hit view page
    """
    all_items = Assignment.objects.all()
    return render(request, 'hit.html', {"all_items": all_items})
