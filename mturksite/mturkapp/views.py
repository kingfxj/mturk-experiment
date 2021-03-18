from .forms import *
from .models import Hit, Hittype, Qualification, Experiment
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .mturk_client import mturk_client
from django_countries import countries
from django_countries.fields import CountryField

# Create your views here.
@login_required
def loginView(request):
    return render(request, 'asgmtsCompleted.html')


def signupView(request):
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
    mturk = mturk_client()
    balance = mturk.get_account_balance()

    return render(request, 'home.html', {"balance": balance})


def hittypesView(request):
    """
    Hittype View Page
    :param request
    :return: Hittype view page
    """
    hittype_items = Hittype.objects.all()
    if request.method == "POST":
        title = request.POST.get('title')                   # Retrieve query for title
        hittype_id = request.POST.get('hittype_id')         # Retrieve query for hittype id
        description = request.POST.get('description')       # Retrieve query for description
        keyword = request.POST.get('keyword')               # Retrieve query for keyword
        reward = request.POST.get('reward')                 # Retrieve query for reward
        quals = request.POST.get('quals')                   # Retrieve query for qualifications
        # Filter the objects according to the sort
        if title != '' and title is not None:
            hittype_items = hittype_items.filter(title__icontains=title)
        if hittype_id != '' and hittype_id is not None:
            hittype_items = hittype_items.filter(hittype_id__icontains=hittype_id)
        if description != '' and description is not None:
            hittype_items = hittype_items.filter(description__icontains=description)
        if keyword != '' and keyword is not None:
            hittype_items = hittype_items.filter(keyword__icontains=keyword)
        if reward != '' and reward is not None:
            hittype_items = hittype_items.filter(reward__icontains=reward)
        if quals != '' and quals is not None:
            hittype_items = hittype_items.filter(quals__icontains=quals)
    # Return the objects that satisfy all search filter
    return render(request, 'hittypes/hittypes.html', {"hittype_items": hittype_items})


def addHittypeView(request):
    """
    Add a new HITType
    :param request
    :return: Redirect to HITType View page after changes are made
    """
    mturk = mturk_client()
    qualifications = mturk.list_qualification_types(  # api call gets all qualifications created by the admin
        MustBeRequestable=False,
        MustBeOwnedByCaller=True,
    )
    if request.method == "POST":
        form = HittypeForm(request.POST or None)       
        if form.is_valid():            
            title = form.cleaned_data.get("title")                   # Retrieve query for title  
            description = form.cleaned_data.get("description")       # Retrieve query for description
            keyword = form.cleaned_data.get("keyword")               # Retrieve query for keyword
            reward = form.cleaned_data.get("reward")                 # Retrieve query for reward
            quals = form.cleaned_data.get("quals")                   # Retrieve query for qualifications

            hittypes = mturk.create_hit_type(
                AssignmentDurationInSeconds = 2345,
                Reward = reward,
                Title = title,
                Keywords = keyword,
                Description = description
                )
            instance = form.save()
            hittype_id = Hittype(hittype_id = hittypes["HITTypeId"], 
                title = title , 
                description = description , 
                keyword = keyword , 
                reward = reward , 
                quals = quals)
            hittype_id.pk = instance.pk
            hittype_id.save()
            messages.success(request, "Item has been added!")
            return redirect(hittypesView)
        else:
            messages.error(request, "Item was not added")
            return redirect(hittypesView)
    else:
       context = {"qualifications": qualifications['QualificationTypes']}
       return render(request, 'hittypes/addHittype.html', context)


def hitsView(request):
    """
    Hit View Page
    :param request
    :return: Hit view page
    """
    hit_items = Hit.objects.all()
    if request.method == "POST":
        hit_id = request.POST.get('hit_id')                             # Retrieve query for hit id
        hittype_id = request.POST.get('hittype_id')                     # Retrieve query for hittype id
        max_assignments = request.POST.get('max_assignments')           # Retrieve query for assignments number
        lifetime_in_seconds = request.POST.get('lifetime_in_seconds')   # Retrieve query for expiry date

        # Filter the objects according to the sort
        if hit_id != '' and hit_id is not None:
            hit_items = hit_items.filter(hit_id__icontains=hit_id)
        if hittype_id != '' and hittype_id is not None:
            hit_items = hit_items.filter(hittype_id__icontains=hittype_id)
        if max_assignments != '' and max_assignments is not None:
            hit_items = hit_items.filter(max_assignments__icontains=max_assignments)
        if lifetime_in_seconds != '' and lifetime_in_seconds is not None:
            hit_items = hit_items.filter(lifetime_in_seconds__icontains=lifetime_in_seconds)

    # Return the objects that satisfy all search filter
    return render(request, 'hits/hits.html', {"hit_items": hit_items})


def addHitView(request):
    """
    Add a new HIT
    :param request
    :return: Redirect to HIT View page after changes are made
    """
    game = str(settings.BASE_DIR) + "/mturkapp/templates/games/mine.xml"

    question = open(game).read()
    hittype_items = Hittype.objects.all()    
    if request.method == "POST":
        form = HitForm(request.POST or None)
        if form.is_valid():

            maxassignments = form.cleaned_data.get("max_assignments")
            lifetime_in_seconds = form.cleaned_data.get("lifetime_in_seconds")
            x = form.cleaned_data.get("hittype")
            hittypes = Hittype.objects.get(pk = x)
    
            mturk = mturk_client()
            hit = mturk.create_hit_with_hit_type(
                HITTypeId = hittypes.hittype_id,
                MaxAssignments = maxassignments ,
                LifetimeInSeconds= int(lifetime_in_seconds),
                Question =question
            )
            instance = form.save()
            hit_id = Hit(hit_id = hit["HIT"]["HITId"], 
                hittype_id = hittypes.hittype_id  , 
                max_assignments = maxassignments , 
                lifetime_in_seconds = lifetime_in_seconds 
            )
            hit_id.pk = instance.pk
            hit_id.save()
            messages.success(request, "Item has been added!")
            return redirect(hitsView)
        else:
            messages.error(request, "Item was not added")
            return redirect(hitsView)
    else:
        context = {"hittype_items":hittype_items}
        return render(request, 'hits/addHit.html', context)


def qualificationsView(request):
    """
    Qualification View Page
    :param request
    :return: Qualification view page
    """
    mturk = mturk_client()
    qual_fields = ['nickname', 'description', 'comparator', 'int_value', 'country', 'subdivision']
    qual_info = []

    qualifications = mturk.list_qualification_types(  # api call gets all qualifications created by the admin
        MustBeRequestable=False,
        MustBeOwnedByCaller=True
    )

    if request.method == "POST":
        for field in qual_fields:
            qual_info.append(request.POST.get(field))

        # Filter the objects according to the sort
        if qual_info[0] != '' and qual_info[0] is not None:
            qualifications = qualifications.filter(nickname__icontains=qual_info[0])
        if qual_info[1] != '' and qual_info[1] is not None:
            qualifications = qualifications.filter(qualID__icontains=qual_info[1])
        if qual_info[2] != '' and qual_info[2] is not None:
            qualifications = qualifications.filter(comparator__icontains=qual_info[2])
        if qual_info[3] != '' and qual_info[3] is not None:
            qualifications = qualifications.filter(int_value__icontains=qual_info[3])
        if qual_info[4] != '' and qual_info[4] is not None:
            qualifications = qualifications.filter(country__icontains=qual_info[4])
        if qual_info[5] != '' and qual_info[5] != None:
            qualifications = qualifications.filter(subdivision__icontains=qual_info[5])

    # Return the objects that satisfy all search filter
    return render(request, 'qualifications/qualifications.html', {"qualifications": qualifications['QualificationTypes']})


def addQualificationView(request):
    """
    Add a new qualification
    :param request
    :return: Redirect to Assignment View page after changes are made
    """
    mturk = mturk_client()

    country_list = []
    for code, name in list(countries):
        country_list.append(name)

    qual_fields = ['nickname', 'description', 'comparator', 'int_value', 'country', 'subdivision']
    if request.method == "POST":
        form = QualificationForm(request.POST or None)

        if form.is_valid():
            #sorting data from fields
            qual_info = []
            for i in qual_fields:
                qual_info.append(form.cleaned_data[i])
            
            print(qual_info)

            #api call to create qualification type
            response = mturk.create_qualification_type(
                Name= qual_info[0],
                Description= qual_info[1],
                QualificationTypeStatus='Active')
            print("QUALIFICATION: ", response)
            messages.success(request, "Item has been added!")
            return redirect(qualificationsView)
        else:
            messages.error(request, "Item was not added")
            return redirect(qualificationsView)
    else:
        context = {"country": country_list}
        return render(request, 'qualifications/addQualification.html', context)


def updateQualificationView(request,List_id):

    mturk = mturk_client()

    qualifications = mturk.list_qualification_types(  # api call gets all qualifications created by the admin
        MustBeRequestable=False,
        MustBeOwnedByCaller=True,
    )
    print(List_id)
    for x in qualifications['QualificationTypes']:
        x['QualificationTypeId'] = List_id
        if x['QualificationTypeStatus'] == 'Inactive':
            up = mturk.update_qualification_type(
                   QualificationTypeId= List_id,
                   QualificationTypeStatus='Active'
                  )
        else:
            up = mturk.update_qualification_type(
                    QualificationTypeId= List_id,
                    QualificationTypeStatus='Inactive'
                 )

    messages.success(request, "Item has been Updated!")
    return redirect('qualifications')


def asgmtsActiveView(request):
    """
    View Active assignment
    :param request
    :return: Active assignment page
    """   

    mturk = mturk_client()
    assignments = mturk.list_assignments_for_hit(HITId='3G3AJKPCXLNWBAVG53KG569HGW24YI')['Assignments']

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
    return render(request, 'assignments/asgmtsActive.html', {"assignments": assignments})


def asgmtsCompletedView(request):
    """
    View Completed assignments
    :param request
    :return: Completed assignments page
    """   

    mturk = mturk_client()
    assignments = mturk.list_assignments_for_hit(HITId='3G3AJKPCXLNWBAVG53KG569HGW24YI')['Assignments']

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
    return render(request, 'assignments/asgmtsCompleted.html', {"assignments": assignments})


def payBonusView(request):
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

    return render(request, 'assignments/payBonuses.html', {"all_items": all_items})
    

def lobbyView(request):
    """
    Lobby View Page
    :param request
    :return: Lobby view page
    """
    # all_items = Assignment.objects.all()
    return render(request, 'lobby/lobby.html')


def experimentsView(request):
    """
    Experiments view Page
    :param request
    :return: Experiments view page
    """
    experiment_items = Experiment.objects.all()
    if request.method == "POST":
        title = request.POST.get('title')             # Retrieve query for experiments id
        batch_id = request.POST.get('batch_id') 

        # Filter the objects according to the sort
        if title != '' and title is not None:
            experiment_items = experiment_items.filter(title__icontains=title)
        if batch_id != '' and batch_id is not None:
            experiment_items = experiment_items.filter(batch_id__icontains=batch_id)

    # Return the objects that satisfy all search filter
    return render(request, 'experiments/experiments.html', {"experiment_items": experiment_items})


def addExperimentView(request):
    """
    Add a new experiment
    :param request
    :return: Redirect to experiment View page after changes are made
    """

    if request.method == "POST":
        form = ExperimentForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Item has been added!")
            return redirect(experimentsView)
        else:
            messages.error(request, "Item was not added")
            return redirect(experimentsView)
    else:
        return render(request, 'experiments/addExperiment.html')

def workersView(request):
    """
    Experiments view Page
    :param request
    :return: Experiments view page
    """
    mturk = mturk_client()
    workers_list = []
    hittypeid_list = []
    # all_items = HITType.objects.get(hittype_id=)   
    for i in Hit.objects.all():
        # print(type(i.hittype_id))
        hittypeid_list.append(i.hittype_id)
        # print("hittype ids: ", type(i))

    # response = mturk.list_assignments_for_hit(
    # HITId='38TZTS8OLOLLVWMMJU4ONQY3AU5U3X',
    # AssignmentStatuses=['Submitted', 'Approved', 'Rejected'])
    # print("RESPONSE: ", response['Assignments'][0]['WorkerId'])

    for id in hittypeid_list:
        try:
            response = mturk.list_assignments_for_hit(
                HITId='38TZTS8OLOLLVWMMJU4ONQY3AU5U3X',
                AssignmentStatuses=['Submitted', 'Approved', 'Rejected'])
            workers_list.append(response['Assignments'][0]['WorkerId'])
            print("RESPONSE: ", response['Assignments'][0]['WorkerId'])
        except:
            print("Couldn't find", id)
        


    if request.method == "POST" or None:
        pass
        # for id in hittypeid_list:
        #     print("ID: ", id)
        #     try:
        #         response = mturk.list_assignments_for_hit(
        #             HITId=id,
        #             AssignmentStatuses=['Submitted', 'Approved', 'Rejected'])
        #         workers_list.append(response['Assignments'][0]['WorkerId'])
        #         print("RESPONSE: ", response['Assignments'][0]['WorkerId'])
        #     except:
        #         print("Couldn't find", id)
    else:
        # Return the objects that satisfy all search filter
        # all_items = HITType.objects.all()
        return render(request, 'workers.html', {"workers": workers_list})
  