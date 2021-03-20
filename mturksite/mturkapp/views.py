from .forms import *
from .models import *
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .mturk_client import mturk_client
from django_countries import countries
from django_countries.fields import CountryField

# display signup page
def signupView(request):
    if request.method == 'POST':
        # signup form
        form = SignUpForm(request.POST)
        # set variables
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            user.is_staff = True
            user.is_superuser = True
            user.save()
            login(request, user)
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

# display home page - shows account balance 
def homeView(request):
    """
    Home View
    :param request
    :return: Home page
    """
    # get balance and return
    mturk = mturk_client()
    balance = mturk.get_account_balance()
    return render(request, 'home.html', {"balance": balance})

# display hittypes table 
def hittypesView(request):
    """
    Hittype View Page
    :param request
    :return: Hittype view page
    """
    # retrieve all hittype objects
    hittype_items = Hittype.objects.all().order_by('-id')
    # retrieve queries for all hittype fields
    if request.method == "POST":
        title = request.POST.get('title')               
        hittype_id = request.POST.get('hittype_id')       
        description = request.POST.get('description')      
        keyword = request.POST.get('keyword')             
        reward = request.POST.get('reward')                
        qualifications = request.POST.get('qualifications')
        batch = request.POST.get('batch')                   
        # filter the objects according to the sort
        if title != '' and title is not None:
            hittype_items = hittype_items.filter(title__icontains=title)
        if hittype_id != '' and hittype_id is not None:
            hittype_items = hittype_items.filter(hittype_id__icontains=hittype_id)
        if description != '' and description is not None:
            hittype_items = hittype_items.filter(description__icontains=description)
        if keyword != '' and keyword is not None:
            hittype_items = hittype_items.filter(keyword__icontains=keyword)
        if qualifications != '' and qualifications is not None:
            hittype_items = hittype_items.filter(qualifications__icontains=qualifications)
        if batch != '' and batch is not None:
            hittype_items = hittype_items.filter(batch__icontains=batch)
    # return the objects that satisfy all search filters
    return render(request, 'hittypes/hittypes.html', {"hittype_items": hittype_items})

# display add hittype form page
def addHittypeView(request):
    """
    Add a new HITType
    :param request
    :return: Redirect to HITType View page after changes are made
    """
    # api call - gets all qualifications created by admin
    mturk = mturk_client()
    qualifications = mturk.list_qualification_types(  
        MustBeRequestable=False,
        MustBeOwnedByCaller=True,
    )
    if request.method == "POST":
        # hittype form
        form = HittypeForm(request.POST or None)       
        if form.is_valid():    
            # retrieve queries for all adding hittype fields        
            title = form.cleaned_data.get("title")                                           
            description = form.cleaned_data.get("description")                                   
            keyword = form.cleaned_data.get("keyword")                                             
            reward = form.cleaned_data.get("reward")                                               
            choice = form.cleaned_data.get("qualifications")                                         
            batch = form.cleaned_data.get("batch")                                                    
            Assignment_Duration_In_Seconds = form.cleaned_data.get("Assignment_Duration_In_Seconds")  
            Auto_Approval_Delay_In_Seconds = form.cleaned_data.get("Auto_Approval_Delay_In_Seconds")  
            # remove special characters that appears when more than one qualification is selected
            characters_to_remove = "[]''"                    
            new_string = choice
            for word in characters_to_remove:
                new_string = new_string.replace(word,"")
            qualifications = new_string
            # adding in batch id
            experiment_items = Experiment.objects.all()
            for item in experiment_items:
                if str(item.batch_id) in batch:
                    batch_title = item.title
                    batch_id = item.batch_id
                    break
            # api call - create hittype
            hittypes = mturk.create_hit_type(
                AutoApprovalDelayInSeconds = Auto_Approval_Delay_In_Seconds,
                AssignmentDurationInSeconds = Assignment_Duration_In_Seconds ,
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
                qualifications = qualifications,
                batch_id = batch_id,
                batch_title = batch_title
            )
            hittype_id.pk = instance.pk
            hittype_id.save()
            messages.success(request, "Item has been added!")
            return redirect(hittypesView)
        else:
            messages.error(request, "Item was not added")
            return redirect(hittypesView)
    else:
        experiment_items = Experiment.objects.all()
        context = {"qualifications": qualifications['QualificationTypes'], "experiment_items": experiment_items}
        return render(request, 'hittypes/addHittype.html', context)

# display hits table
def hitsView(request):
    """
    Hit View Page
    :param request
    :return: Hit view page
    """
    # retrieve all hit objects and sort
    hit_items = Hit.objects.all().order_by('-id')
    # retrieve queries for all hit fields
    if request.method == "POST":
        hit_id = request.POST.get('hit_id')                          
        hittype_id = request.POST.get('hittype_id')               
        max_assignments = request.POST.get('max_assignments')         
        lifetime_in_seconds = request.POST.get('lifetime_in_seconds')  
        # filter the objects according to the sort
        if hit_id != '' and hit_id is not None:
            hit_items = hit_items.filter(hit_id__icontains=hit_id)
        if hittype_id != '' and hittype_id is not None:
            hit_items = hit_items.filter(hittype_id__icontains=hittype_id)
        if max_assignments != '' and max_assignments is not None:
            hit_items = hit_items.filter(max_assignments__icontains=max_assignments)
        if lifetime_in_seconds != '' and lifetime_in_seconds is not None:
            hit_items = hit_items.filter(lifetime_in_seconds__icontains=lifetime_in_seconds)
    # return the objects that satisfy all search filters
    return render(request, 'hits/hits.html', {"hit_items": hit_items})

# display add hits form page 
def addHitView(request):
    """
    Add a new HIT
    :param request
    :return: Redirect to HIT View page after changes are made
    """
    # question form
    game = str(settings.BASE_DIR) + "/mturkapp/templates/games/mine.xml"
    question = open(game).read()
    # retrieve all hittype objects
    hittype_items = Hittype.objects.all()    
    if request.method == "POST":
        # hit form
        form = HitForm(request.POST or None)
        if form.is_valid():
            # retrieve queries for all adding hit fields
            maxassignments = form.cleaned_data.get("max_assignments")
            lifetime_in_seconds = form.cleaned_data.get("lifetime_in_seconds")
            x = form.cleaned_data.get("hittype")
            hittypes = Hittype.objects.get(pk = x)
            # api call - create hit with hittype
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

# display qualifications table
def qualificationsView(request):
    """
    Qualification View Page
    :param request
    :return: Qualification view page
    """
    mturk = mturk_client()
    qual_fields = ['nickname', 'description', 'comparator', 'int_value', 'country', 'subdivision']
    qual_info = []

    try:
        qualifications = mturk.list_qualification_types(  # api call gets all qualifications created by the admin
            MustBeRequestable=False,
            MustBeOwnedByCaller=True)
    except mturk.exceptions.ServiceFault:
        messages.error(request, "API Service Fault")
    except mturk.exceptions.RequestError:
        messages.error(request, "Unable to get qualification types")
    
    # TODO show both active/inactive qual types
    # print("API: ", qualifications['QualificationTypes'])
    # qual_objects = Qualification.objects.all()
    # for item in qual_objects:
    #     print("OBJECT: ", item)

    if request.method == "POST":
        # append selected fields
        for field in qual_fields:
            qual_info.append(request.POST.get(field))
        # filter the objects according to the sort
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
    # return the objects that satisfy all search filters
    return render(request, 'qualifications/qualifications.html', {"qualifications": qualifications['QualificationTypes']})

# display add qualifiction form page
def addQualificationView(request):
    """
    Add a new qualification
    :param request
    :return: Redirect to Assignment View page after changes are made
    """
    mturk = mturk_client()

    qual_fields = ['nickname', 'description', 'comparator', 'int_value', 'country', 'subdivision']  # init list of qualification fields
    country_list = []  # init country list
    for name in list(countries):
        country_list.append(name)

    if request.method == "POST":
        # qualifiction form
        form = QualificationForm(request.POST or None)
        if form.is_valid():
            qual_info = []  # init field data list
            for i in qual_fields:
                qual_info.append(form.cleaned_data[i])

            try:
                response = mturk.create_qualification_type(  # api call to create qualification type
                    Name= qual_info[0],
                    Description= qual_info[1],
                    QualificationTypeStatus='Active')

                new_qualification = Qualification(  # create qualification object and store on db
                    nickname = response['QualificationType']['Name'],
                    description = response['QualificationType']['Description'],
                    QualificationTypeId = response['QualificationType']['QualificationTypeId'],
                    comparator = qual_info[2],
                    int_value = qual_info[3],
                    country = qual_info[4],
                    subdivision = qual_info[5],
                    status = response['QualificationType']['QualificationTypeStatus'])

                instance = form.save()
                new_qualification.pk = instance.pk
                new_qualification.save()
                messages.success(request, "Item has been added!")

            except mturk.exceptions.ServiceFault:  # error handling for ServiceFault, RequestError
                messages.error(request, "API Service Fault")
            except mturk.exceptions.RequestError:
                messages.error(request, "Failed to create qualification type")
            except:
                messages.error(request, "Unexpected Error")

            return redirect(qualificationsView)
        else:
            messages.error(request, "Item was not added")
            return redirect(qualificationsView)
    else:
        context = {"country": country_list}
        return render(request, 'qualifications/addQualification.html', context)


def updateQualificationView(request, List_id):
    mturk = mturk_client()

    try: 
        qualifications = mturk.list_qualification_types(  # api call retrieves all qualifications created by the admin
            MustBeRequestable=False,
            MustBeOwnedByCaller=True,)
    except mturk.exceptions.ServiceFault:  # error handling for ServiceFault, RequestError
        messages.error(request, "API Service Fault")
    except mturk.exceptions.RequestError:
        messages.error(request, "Unable to get qualification types")

    # print("LIST ID: ", List_id)  # print check

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

# display workers table
def workersView(request):
    """
    Workers view Page
    :param request
    :return: Workers view page
    """
    # retrieve all hit IDs
    mturk = mturk_client()
    workers_list = []
    hitID_list = []
    for i in Hit.objects.all(): 
        hitID_list.append(i.hit_id)
    # retrieve all assignments for that hit ID
    for id in hitID_list:
        try:
            response = mturk.list_assignments_for_hit(
                HITId=id,
                AssignmentStatuses=['Submitted', 'Approved', 'Rejected'])
            workers_list.append(response['Assignments'][0])
        except:
            print("Couldn't find", id)
        
    if request.method == "POST" or None:
        pass  #TODO add assigning qual to workers functionality
    else:
        return render(request, 'workers/workers.html', {"workers": workers_list})

# display active assignments table
def asgmtsActiveView(request):
    """
    View Active assignment
    :param request
    :return: Active assignment page
    """   
    # filter by experiment
    experimentFilter = request.session['experiment'] if ('experiment' in request.session) else ""
    # select all hittype objects accordingly
    hittype_items = Hittype.objects.all()
    hittypes_filtered = []
    for item in hittype_items:
        if str(item.batch_id) in experimentFilter:
            hittypes_filtered.append(str(item.hittype_id))
    # select all hit objects accordingly
    hit_items = Hit.objects.all()
    hits_filtered = []
    for item in hit_items:
        if str(item.hittype_id) in hittypes_filtered:
            hits_filtered.append(str(item.hit_id))
    # select all assignments (from api call) accordingly
    mturk = mturk_client()
    assignments = []
    for hit_id in hits_filtered:
        for assignment in mturk.list_assignments_for_hit(HITId=hit_id)['Assignments']:
            assignments.append(assignment)
    # retrieve queries for all assignment fields
    if request.method == "POST":
        assignmentIdFilter = request.POST.get('assignmentId')   
        workerIdFilter = request.POST.get('workerId')          
        acceptTimeFilter = request.POST.get('acceptanceTime')  
        submitTimeFilter = request.POST.get('submittedTime')    
        statusFilter = request.POST.get('status')             
        # filter the objects according to the sort
        if assignmentIdFilter != '' and assignmentIdFilter is not None:
            for assignment in assignments:
                if assignmentIdFilter not in assignment['AssignmentId']:
                    assignments.remove(assignment)
        if workerIdFilter != '' and workerIdFilter is not None:
            for assignment in assignments:
                if  workerIdFilter not in assignment['WorkerId']:
                    assignments.remove(assignment)
        if acceptTimeFilter != '' and acceptTimeFilter is not None:
            for assignment in assignments:
                if acceptTimeFilter not in assignment['AcceptTime']:
                    assignments.remove(assignment)
        if submitTimeFilter != '' and submitTimeFilter is not None:
            for assignment in assignments:
                if submitTimeFilter not in assignment['SubmitTime']:
                    assignments.remove(assignment)
        if statusFilter != '' and statusFilter is not None:
            for assignment in assignments:
                if statusFilter not in assignment['AssignmentStatus']:
                    assignments.remove(assignment)
    # return the objects that satisfy all search filters
    return render(request, 'assignments/asgmtsActive.html', {"assignments": assignments})

# display completed assignments table 
def asgmtsCompletedView(request):
    """
    View Completed assignments
    :param request
    :return: Completed assignments page
    """   
    # filter by experiment
    experimentFilter = request.session['experiment'] if ('experiment' in request.session) else ""
    # select all hittype objects accordingly
    hittype_items = Hittype.objects.all()
    hittypes_filtered = []
    for item in hittype_items:
        if str(item.batch_id) in experimentFilter:
            hittypes_filtered.append(str(item.hittype_id))
    # select all hit objects accordingly
    hit_items = Hit.objects.all()
    hits_filtered = []
    for item in hit_items:
        if str(item.hittype_id) in hittypes_filtered:
            hits_filtered.append(str(item.hit_id))
    # select all assignments (from api call) accordingly
    mturk = mturk_client()
    assignments = []
    for hit_id in hits_filtered:
        for assignment in mturk.list_assignments_for_hit(HITId=hit_id)['Assignments']:
            assignments.append(assignment)
    # retrieve queries for all assignment fields
    if request.method == "POST":
        assignmentIdFilter = request.POST.get('assignmentId')  
        workerIdFilter = request.POST.get('workerId')          
        acceptTimeFilter = request.POST.get('acceptanceTime')  
        submitTimeFilter = request.POST.get('submittedTime')   
        statusFilter = request.POST.get('status')              
        # filter the objects according to the sort
        if assignmentIdFilter != '' and assignmentIdFilter is not None:
            for assignment in assignments:
                if assignmentIdFilter not in assignment['AssignmentId']:
                    assignments.remove(assignment)
        if workerIdFilter != '' and workerIdFilter is not None:
            for assignment in assignments:
                if  workerIdFilter not in assignment['WorkerId']:
                    assignments.remove(assignment)
        if acceptTimeFilter != '' and acceptTimeFilter is not None:
            for assignment in assignments:
                if acceptTimeFilter not in assignment['AcceptTime']:
                    assignments.remove(assignment)
        if submitTimeFilter != '' and submitTimeFilter is not None:
            for assignment in assignments:
                if submitTimeFilter not in assignment['SubmitTime']:
                    assignments.remove(assignment)
        if statusFilter != '' and statusFilter is not None:
            for assignment in assignments:
                if statusFilter not in assignment['AssignmentStatus']:
                    assignments.remove(assignment)
    # return the objects that satisfy all search filters
    return render(request, 'assignments/asgmtsCompleted.html', {"assignments": assignments})

# pay bonuses
def payBonusView(request):
    """
    Pay Bonus
    :param request
    :return:
    NOT IMPLEMENTED
    """
    # # retrieve assignment IDs
    # selectPayment = request.session.get('payBonus', None)
    # if not selectPayment:
    #     selectPayment = []
    # all_items = Assignment.objects.filter(id__in=selectPayment)
    # # retrieve queries for all fields
    # if request.method == "POST":
    #     name = request.POST.get('name')            
    #     surname = request.POST.get('surname')     
    #     birthYear = request.POST.get('birthYear')   
    #     birthCity = request.POST.get('birthCity')   
    #     active = request.POST.get('active')         
    #     # remove that ID from payment
    #     for key in request.POST.keys():
    #         if key.startswith('deletePayment'):
    #             action = key[14:]
    #             selectPayment.remove(action)
    #             request.session['payBonus'] = selectPayment
    #             all_items = Assignment.objects.filter(id__in=selectPayment)
    #     # filter the objects according to the sort
    #     if name != '' and name is not None:
    #         all_items = all_items.filter(name__icontains=name)
    #     if surname != '' and surname is not None:
    #         all_items = all_items.filter(surname__icontains=surname)
    #     if birthYear != '' and birthYear is not None:
    #         all_items = all_items.filter(birthYear__icontains=birthYear)
    #     if birthCity != '' and birthCity is not None:
    #         all_items = all_items.filter(birthCity__icontains=birthCity)
    #     if active != '' and active is not None:
    #         all_items = all_items.filter(active__icontains=active)
    # return render(request, 'assignments/payBonuses.html', {"all_items": all_items})

# display users and their status in current lobby
def lobbyView(request):
    """
    Lobby View Page
    :param request
    :return: Lobby view page
    """
    # retrieve all hit IDs
    mturk = mturk_client()
    lobby_list = []
    hitID_list = []
    for i in Hit.objects.all():         
        hitID_list.append(i.hit_id)
    # retrieve all assignments for that hit ID
    for id in hitID_list:
        try:
            response = mturk.list_assignments_for_hit(HITId=id)
            lobby_list.append(response['Assignments'][0])
        except:
            print("Couldn't find", id)
    # find total number of users in lobby
    total_users=len(lobby_list)   
    # find number of 'ready' users in lobby                          
    ready_users=0
    for item in lobby_list:                                 
        if item['AssignmentStatus'] == 'Approved':
            ready_users += 1
    return render(request, 'lobby/lobby.html', {"lobby": lobby_list,"total_users": total_users, "ready_users": ready_users})

# display experiments table
def experimentsView(request):
    """
    Experiments view Page
    :param request
    :return: Experiments view page
    """
    # retrieve all experiment objects
    experiment_items = Experiment.objects.all()
    if request.method == "POST":
        # retrieve queries for all experiment fields
        batch_id = request.POST.get('batch_id')        
        title = request.POST.get('title')              
        # filter the objects according to the sort
        if batch_id != '' and batch_id is not None:
            experiment_items = experiment_items.filter(batch_id__icontains=batch_id)
        if title != '' and title is not None:
            experiment_items = experiment_items.filter(title__icontains=title)
    # return the objects that satisfy all search filters
    return render(request, 'experiments/experiments.html', {"experiment_items": experiment_items})

# display add experiment form page
def addExperimentView(request):
    """
    Add a new experiment
    :param request
    :return: Redirect to experiment View page after changes are made
    """
    if request.method == "POST":
        # experiment form
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

# display filter experiment page
def experimentFilterView(request):
    """
    Filter application by experiment using session
    :param request
    :return: Redirect to previous page after changes are made
    """
    # get batch ID and return experiments' title (ID)
    if request.method == "POST":
        experiment = request.POST.get('batch')
        request.session['experiment'] = experiment
        return redirect(experimentFilterView)
    else:   
        experiment_items = Experiment.objects.all() 
        return render(request, 'experiments/experimentFilter.html', {"experiment_items": experiment_items})

def workersView(request):
    """
    Workers view Page
    :param request
    :return: Workers view page
    """
    mturk = mturk_client()
    workers_list = []
    hitID_list = []
    for i in Hit.objects.all():  #retrieve all hit ids and add it to 
        hitID_list.append(i.hit_id)

    for id in hitID_list:
        try:
            response = mturk.list_assignments_for_hit(  # api call to retrieve all assignments based on hit ID
                HITId=id,
                AssignmentStatuses=['Submitted', 'Approved', 'Rejected'])
            for item in response['Assignments']:
                workers_list.append(item)
            # print("RESPONSE: ", response['Assignments'][0])  # print check
        except mturk.exceptions.RequestError:  # exception raised if hit id not found
            print("Could not retrieve", id)
        except mturk.exceptions.ServiceFault:
            messages.error(request, "API Service Fault")

    return render(request, 'workers/workers.html', {"workers": workers_list})
  
def workerAssignQualView(request, worker_id):
    """
    Workers Assign qualifications view Page
    :param request, worker_id
    :return: Workers view page
    """
    mturk = mturk_client()
    try:  # api call gets all qualifications created by the admin
        qualifications_api = mturk.list_qualification_types(  
            MustBeRequestable=False,
            MustBeOwnedByCaller=True)
    except mturk.exceptions.ServiceFault:
        messages.error(request, "API Service Fault")
    except mturk.exceptions.RequestError:
        messages.error(request, "Unable to get qualification types")

    # api call to assign selected qual need to be in a loop
    try:
        response = mturk.associate_qualification_with_worker(
            QualificationTypeId='string',
            WorkerId='string',
            IntegerValue=123,
            SendNotification=True|False)
    except mturk.exceptions.ServiceFault:
        messages.error(request, "API Service Fault")
    except mturk.exceptions.RequestError:
        messages.error(request, "Unable to assign qualifications")
    except:
        messages.error(request, "Unable to assign qualifications")

    if request.method == "POST":
        # form = AssignQualForm(request.POST or None)
        # if form.is_valid():
            # qual = form.cleaned_data.get("qualifications")\
        pass
    else:
        # return render(request, '/workers')
        return redirect('/workers')
