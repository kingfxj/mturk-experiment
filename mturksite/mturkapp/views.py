from .forms import SignUpForm, hitForm, hittypeForm, qualificationForm
from .models import HIT, HITType, Qualification
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .mturk_client import mturk_client
import xml.dom.minidom


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
    all_items = Qualification.objects.all() 
    if request.method == "POST":
        form = qualificationForm(request.POST or None)
        if form.is_valid():
            nickname = form.cleaned_data.get('nickname')
            comparator = form.cleaned_data.get('comparator')
            int_value = form.cleaned_data.get('int_value')
            description = form.cleaned_data.get('description')               
            country = form.cleaned_data.get('country')                   
            subdivision = form.cleaned_data.get('subdivision')           
            actions_guarded = form.cleaned_data.get('actions_guarded') 
            
            mturk = mturk_client()
            qual = mturk.create_qualification_type(
               Name= nickname,
               Description= description,
               QualificationTypeStatus='Active'                             #,
                                                                                #RetryDelayInSeconds=123
            )
            x = False
            instance = form.save()
            if qual["QualificationType"]["QualificationTypeStatus"] == 'Active':
                x = True
            qualID = Qualification( qualID= qual["QualificationType"]["QualificationTypeId"], 
                comparator= comparator  , 
                int_value = int_value , 
                country = country,
                subdivision = subdivision,
                actions_guarded = actions_guarded,
                nickname = nickname,
                Status = x
            )
            qualID.pk = instance.pk
            qualID.save()
            messages.success(request, "Item has been added!")
            return redirect(qualificationView)
        else:
            messages.error(request, "Item was not added")
            return redirect(qualificationView)
    else:
        context = {"all_items": all_items }
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
            hittypes = mturk.create_hit_type(
                AssignmentDurationInSeconds = 2345,
                Reward = reward,
                Title = title,
                Keywords = keyword,
                Description = description )
            
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
