from .forms import *
from .models import HIT, HITType, Qualification
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .mturk_client import mturk_client
from django_countries import countries
from django_countries.fields import CountryField

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
    assignments = mturk.list_assignments_for_hit(HITId= hit["HIT"]["HITId"])['Assignments']

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
    mturk = mturk_client()
    qual_fields = ['nickname', 'description', 'comparator', 'int_value', 'country', 'subdivision']
    qual_info = []
    # all_items = Qualification.objects.all()
    all_items = mturk.list_qualification_types(  # api call gets all qualifications created by the admin
        MustBeRequestable=False,
        MustBeOwnedByCaller=True,
    )
    # print('all items: ', all_items['QualificationTypes'])  # print check
    if request.method == "POST":
        for field in qual_fields:
            qual_info.append(request.POST.get(field))

        # Filter the objects according to the sort
        if qual_info[0] != '' and qual_info[0] is not None:
            all_items = all_items.filter(nickname__icontains=qual_info[0])
        if qual_info[1] != '' and qual_info[1] is not None:
            all_items = all_items.filter(qualID__icontains=qual_info[1])
        if qual_info[2] != '' and qual_info[2] is not None:
            all_items = all_items.filter(comparator__icontains=qual_info[2])
        if qual_info[3] != '' and qual_info[3] is not None:
            all_items = all_items.filter(int_value__icontains=qual_info[3])
        if qual_info[4] != '' and qual_info[4] is not None:
            all_items = all_items.filter(country__icontains=qual_info[4])
        if qual_info[5] != '' and qual_info[5] != None:
            all_items = all_items.filter(subdivision__icontains=qual_info[5])

    # Return the objects that satisfy all search filter
    return render(request, 'qualification.html', {"all_items": all_items['QualificationTypes']})


def addQualification(request):
    """
    Add a new qualification
    :param request
    :return: Redirect to Assignment View page after changes are made
    """
    mturk = mturk_client()

    # all_items = Qualification.objects.all() 
    all_items = mturk.list_qualification_types(  # api call gets all qualifications created by the admin
        MustBeRequestable=False,
        MustBeOwnedByCaller=True,
    )

    country_list = []
    for code, name in list(countries):
        country_list.append(name)
    # print(countries)

    qual_fields = ['nickname', 'description', 'comparator', 'int_value', 'country', 'subdivision']
    if request.method == "POST":
        form = qualificationForm(request.POST or None)

        if form.is_valid():
            #sorting data from fields
            qual_info = []
            for i in qual_fields:
                qual_info.append(form.cleaned_data[i])

            #api call to create qualification type
            response = mturk.create_qualification_type(
                Name= qual_info[0],
                Description= qual_info[1],
                QualificationTypeStatus='Active')
            print("QUALIFICATION: ", response)
            messages.success(request, "Item has been added!")
            return redirect(qualificationView)
        else:
            messages.error(request, "Item was not added")
            return redirect(qualificationView)
    else:
        context = {"all_items": all_items['QualificationTypes'], "country": country_list}
        return render(request, 'addQualifications.html', context)

def updateQualification(request,List_id):
    all_items = Qualification.objects.get(pk = List_id) 
    mturk = mturk_client()
    if all_items.Status == False:
        up = mturk.update_qualification_type(
               QualificationTypeId= all_items.qualID,
               QualificationTypeStatus='Active'
              )
    else:
        up = mturk.update_qualification_type(
                QualificationTypeId= all_items.qualID,
                QualificationTypeStatus='Inactive'
             )
    x = False
    if up["QualificationType"]["QualificationTypeStatus"] == 'Active':
        x = True
    
    all_items.Status = x
    all_items.save()
    messages.success(request, "Item has been Edited!")
    return redirect('qualificationView')
    

def updateQualification(request,List_id):
    all_items = Qualification.objects.get(pk = List_id) 
    mturk = mturk_client()
    if all_items.Status == False:
        up = mturk.update_qualification_type(
               QualificationTypeId= all_items.qualID,
               QualificationTypeStatus='Active'
              )
    else:
        up = mturk.update_qualification_type(
                QualificationTypeId= all_items.qualID,
                QualificationTypeStatus='Inactive'
             )
    x = False
    if up["QualificationType"]["QualificationTypeStatus"] == 'Active':
        x = True
    
    all_items.Status = x
    all_items.save()
    messages.success(request, "Item has been Edited!")
    return redirect('qualificationView')
    

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
        title = request.POST.get('title')                   # Retrieve query for title
        hittype_id = request.POST.get('hittype_id')        # Retrieve query for hittype id
        description = request.POST.get('description')       # Retrieve query for description
        keyword = request.POST.get('keyword')               # Retrieve query for keyword
        reward = request.POST.get('reward')                 # Retrieve query for reward
        quals = request.POST.get('quals')                   # Retrieve query for quals
        # Filter the objects according to the sort
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
    
    qual_items = Qualification.objects.all()
    if request.method == "POST":
        form = hittypeForm(request.POST or None)       
        if form.is_valid():            
            title = form.cleaned_data.get("title")                   # Retrieve query for title  
            description = form.cleaned_data.get("description")       # Retrieve query for description
            keyword = form.cleaned_data.get("keyword")               # Retrieve query for keyword
            reward = form.cleaned_data.get("reward")                 # Retrieve query for reward
            quals = form.cleaned_data.get("quals")

            x = Qualification.objects.get(pk = quals)
            mturk = mturk_client() 
            if x.int_value is None:
                hittypes = mturk.create_hit_type(
                    AssignmentDurationInSeconds = 2345,
                    Reward = reward,
                    Title = title,
                    Keywords = keyword,
                    Description = description
                )
            instance = form.save()
            hittype_id = HITType(hittype_id = hittypes["HITTypeId"], 
                title = title , 
                description = description , 
                keyword = keyword , 
                reward = reward , 
                quals = x.nickname)
            hittype_id.pk = instance.pk
            hittype_id.save()
            print(quals)
            messages.success(request, "Item has been added!")
            return redirect(hittypeView)
        else:
            messages.error(request, "Item was not added")
            return redirect(hittypeView)
    else:
       all_items = HITType.objects.all()
       context = {"all_items": all_items , "qual_items": qual_items}
       return render(request, 'addHITType.html', context)


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
        max_assignments = request.POST.get('max_assignments')       # Retrieve query for assignments number
        expiry_time = request.POST.get('expiry_time')       # Retrieve query for expiry date

        # Filter the objects according to the sort
        if hit_id != '' and hit_id is not None:
            all_items = all_items.filter(hit_id__icontains=hit_id)
        if hittype_id != '' and hittype_id is not None:
            all_items = all_items.filter(hittype_id__icontains=hittype_id)
        if max_assignments != '' and max_assignments is not None:
            all_items = all_items.filter(max_assignments__icontains=max_ssignments)
        if expiry_time != '' and expiry_time is not None:
            all_items = all_items.filter(expiry_time__icontains=expiry_time)

    # Return the objects that satisfy all search filter
    return render(request, 'hit.html', {"all_items": all_items})


def addHIT(request):
    """
    Add a new HIT
    :param request
    :return: Redirect to HIT View page after changes are made
    """
    question = open(r"C:\Users\saman\Desktop\CMPUT401\MTurk\mturk-experiment\mturk-experiment\mturksite\mturkapp\templates\mine.xml").read()
    hittype_items = HITType.objects.all()    
    if request.method == "POST":
        form = hitForm(request.POST or None)
        if form.is_valid():

            maxassignments = form.cleaned_data.get("max_assignments")
            expiry_time = form.cleaned_data.get("expiry_time")
            x = form.cleaned_data.get("hittype")
            hittypes = HITType.objects.get(pk = x)
    
            mturk = mturk_client()
            hit = mturk.create_hit_with_hit_type(
                HITTypeId = hittypes.hittype_id,
                MaxAssignments = maxassignments ,
                LifetimeInSeconds= int(expiry_time),
                Question =question
            )
            instance = form.save()
            hit_id = HIT(hit_id = hit["HIT"]["HITId"], 
                hittype_id = hittypes.hittype_id  , 
                max_assignments = maxassignments , 
                expiry_time = expiry_time 
            )
            hit_id.pk = instance.pk
            hit_id.save()
            messages.success(request, "Item has been added!")
            return redirect(hitView)
        else:
            messages.error(request, "Item was not added")
            return redirect(hitView)
    else:
        all_items = HIT.objects.all()
        context = {"hittype_items":hittype_items ,"all_items": all_items}
        return render(request, 'addHIT.html', context)
