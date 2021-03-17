from .forms import SignUpForm, hitForm, hittypeForm, qualificationForm
from .models import HIT, HITType, Qualification
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .mturk_client import mturk_client

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
            user = authenticate(username=username, password=raw_password)
            user.is_staff = True
            user.is_superuser = True
            user.save()
            login(request, user)
            return redirect('homeView')
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

    mturk = mturk_client()
    assignments = mturk.list_assignments_for_hit(HITId='PASTE_HITID_HERE')['Assignments']

    if request.method == "POST":
        assignmentIdFilter = request.POST.get('assignmentId')             # Retrieve query for Assignment ID
        workerIdFilter = request.POST.get('workerId')                     # Retrieve query for Worker ID
        acceptanceTimeFilter = request.POST.get('acceptanceTime')         # Retrieve query for Acceptance Time
        assignmentStatusFilter = request.POST.get('assignmentStatus')     # Retrieve query for Assignment Status
        
        # Filter the objects according to the sort
        if assignmentIdFilter != '' and assignmentIdFilter is not None:
            for assignment in assignments:
                if assignmentIdFilter not in assignment['AssignmentId']:
                    assignments.remove(assignment)
        if workerIdFilter != '' and workerIdFilter is not None:
            for assignment in assignments:
                if  workerIdFilter not in assignment['WorkerId']:
                    assignments.remove(assignment)
        if acceptanceTimeFilter != '' and acceptanceTimeFilter is not None:
            for assignment in assignments:
                if acceptanceTimeFilter not in assignment['AcceptTime']:
                    assignments.remove(assignment)
        if assignmentStatusFilter != '' and assignmentStatusFilter is not None:
            for assignment in assignments:
                if assignmentStatusFilter not in assignment['AssignmentStatus']:
                    assignments.remove(assignment)

    # Return the objects that satisfy all search filter
    return render(request, 'assignment.html', {"assignments": assignments})


def payBonus(request):
    """
    Pay Bonus
    :param request
    :return:
    """
    # Retrieve the IDs' of the assignment
    selectPayment = request.session.get('payBonus', None)
    if not selectPayment:
        selectPayment = []

    all_items = Assignment.objects.filter(id__in=selectPayment)

    if request.method == "POST":
        name = request.POST.get('name')             # Retrieve query for name
        surname = request.POST.get('surname')       # Retrieve query for surname
        birthYear = request.POST.get('birthYear')   # Retrieve query for Birth Year
        birthCity = request.POST.get('birthCity')   # Retrieve query for Birth City
        active = request.POST.get('active')         # Retrieve query for active
        # Remove that id from the payment
        for key in request.POST.keys():
            if key.startswith('deletePayment'):
                action = key[14:]
                selectPayment.remove(action)
                request.session['payBonus'] = selectPayment
                all_items = Assignment.objects.filter(id__in=selectPayment)

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

    return render(request, 'payBonus.html', {"all_items": all_items})


def qualificationView(request):
    """
    Qualification View Page
    :param request
    :return: Qualification view page
    """
    all_items = Qualification.objects.all()
    if request.method == "POST":
        nickname = request.POST.get('nickname')                 # Retrieve query for nickname
        qualID = request.POST.get('qualID')                     # Retrieve query for qualID
        comparator = request.POST.get('comparator')             # Retrieve query for comparator
        int_value = request.POST.get('int_value')               # Retrieve query for int_value
        country = request.POST.get('country')                   # Retrieve query for country
        subdivision = request.POST.get('subdivision')           # Retrieve query for subdivision
        actions_guarded = request.POST.get('actions_guarded')   # Retrieve query for actions_guarded

        # Filter the objects according to the sort
        if nickname != '' and nickname is not None:
            all_items = all_items.filter(nickname__icontains=nickname)
        if qualID != '' and nickname is not None:
            all_items = all_items.filter(qualID__icontains=qualID)
        if comparator != '' and comparator is not None:
            all_items = all_items.filter(comparator__icontains=comparator)
        if int_value != '' and int_value is not None:
            all_items = all_items.filter(int_value__icontains=int_value)
        if country != '' and country is not None:
            all_items = all_items.filter(country__icontains=country)
        if subdivision != '' and subdivision != None:
            all_items = all_items.filter(subdivision__icontains=subdivision)
        if actions_guarded != '' and actions_guarded is not None:
            all_items = all_items.filter(actions_guarded__icontains=actions_guarded)

    # Return the objects that satisfy all search filter
    return render(request, 'qualification.html', {"all_items": all_items})


def addQualification(request):
    """
    Add a new qualification
    :param request
    :return: Redirect to Assignment View page after changes are made
    """
    qual_fields = ['nickname', 'description', 'comparator', 'int_value', 'country', 'subdivision']
    if request.method == "POST":
        form = qualificationForm(request.POST or None)

        if form.is_valid():
            qual_info = []
            for i in qual_fields:
                qual_info.append(form.cleaned_data[i])
            create_qualification(qual_info)
            # form.save()
            # messages.success(request, "Item has been added!")
            return redirect(qualificationView)
        else:
            messages.error(request, "Item was not added")
            return redirect(qualificationView)
    else:
        all_items = Qualification.objects.all()
        return render(request, 'addQualifications.html', {"all_items": all_items})

def create_qualification(info):
    mturk = mturk_client()


    response = mturk.create_qualification_type(
        Name= info[0],
        Description= info[1],
        QualificationTypeStatus='Active')
    print(response)


def lobbyView(request):
    """
    Lobby View Page
    :param request
    :return: Lobby view page
    """
    all_items = Assignment.objects.all()
    return render(request, 'lobby.html', {"all_items": all_items})


def hittypeView(request):
    """
    Hittype View Page
    :param request
    :return: Hittype view page
    """
    all_items = HITType.objects.all()
    if request.method == "POST":
        batch = request.POST.get('batch')                   # Retrieve query for batch
        title = request.POST.get('title')                   # Retrieve query for title
        hittype_id = request.POST.get('hittype_id')         # Retrieve query for hittype id
        description = request.POST.get('description')       # Retrieve query for description
        keyword = request.POST.get('keyword')               # Retrieve query for keyword
        reward = request.POST.get('reward')                 # Retrieve query for reward
        quals = request.POST.get('quals')                   # Retrieve query for quals
        # Filter the objects according to the sort
        if batch != '' and batch is not None:
            all_items = all_items.filter(batch__icontains=batch)
        if title != '' and title is not None:
            all_items = all_items.filter(title__icontains=title)
        if hittype_id != '' and hittype_id is not None:
            all_items = all_items.filter(hittype_id__icontains=hittype_id)
        if description != '' and description is not None:
            all_items = all_items.filter(description__icontains=description)
        if keyword != '' and keyword is not None:
            all_items = all_items.filter(keyword__icontains=keyword)
        if reward != '' and reward is not None:
            all_items = all_items.filter(reward__icontains=reward)
        if quals != '' and quals is not None:
            all_items = all_items.filter(quals__icontains=quals)
    # Return the objects that satisfy all search filter
    return render(request, 'hittype.html', {"all_items": all_items})


def addHITType(request):
    """
    Add a new HITType
    :param request
    :return: Redirect to HITType View page after changes are made
    """
    if request.method == "POST":
        form = hittypeForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Item has been added!")
            return redirect(hittypeView)
        else:
            messages.error(request, "Item was not added")
            return redirect(hittypeView)
    else:
        all_items = HITType.objects.all()
        return render(request, 'addHITType.html', {"all_items": all_items})


def hitView(request):
    """
    Hit View Page
    :param request
    :return: Hit view page
    """
    all_items = HIT.objects.all()
    if request.method == "POST":
        hit_id = request.POST.get('hit_id')                 # Retrieve query for hit id
        hittype_id = request.POST.get('hittype_id')         # Retrieve query for hittype id
        assignments = request.POST.get('assignments')       # Retrieve query for assignments number
        expiry_date = request.POST.get('expiry_date')       # Retrieve query for expiry date

        # Filter the objects according to the sort
        if hit_id != '' and hit_id is not None:
            all_items = all_items.filter(hit_id__icontains=hit_id)
        if hittype_id != '' and hittype_id is not None:
            all_items = all_items.filter(hittype_id__icontains=hittype_id)
        if assignments != '' and assignments is not None:
            all_items = all_items.filter(assignments__icontains=assignments)
        if expiry_date != '' and expiry_date is not None:
            all_items = all_items.filter(expiry_date__icontains=expiry_date)

    # Return the objects that satisfy all search filter
    return render(request, 'hit.html', {"all_items": all_items})


def addHIT(request):
    """
    Add a new HIT
    :param request
    :return: Redirect to HIT View page after changes are made
    """
    if request.method == "POST":
        form = hitForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Item has been added!")
            return redirect(hitView)
        else:
            messages.error(request, "Item was not added")
            return redirect(hitView)
    else:
        all_items = HIT.objects.all()
        return render(request, 'addHIT.html', {"all_items": all_items})
