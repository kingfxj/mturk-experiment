from .forms import *
from .models import *
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.clickjacking import xframe_options_exempt
from .mturk_client import mturk_client
from django_countries import countries
from django_countries.fields import CountryField
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_control
import random

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
    # filter by experiment
    experimentFilter = request.session['experiment'] if ('experiment' in request.session) else ""
    # select all hittype objects accordingly
    hittypes_filtered = []
    for item in hittype_items:
        if str(item.batch_id) in experimentFilter:
            hittypes_filtered.append(item)
    hittype_items = hittypes_filtered
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
    # paginate by 5
    paginator = Paginator(hittype_items, 5)
    page_number = request.GET.get('page')
    hittype_page = paginator.get_page(page_number)
    # return the objects that satisfy all search filters
    return render(request, 'hittypes/hittypes.html', {"hittypes" : hittype_page})

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
            hits_filtered.append(item)
    hit_items = hits_filtered
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
    # paginate by 10
    paginator = Paginator(hit_items, 10)
    page_number = request.GET.get('page')
    hit_page = paginator.get_page(page_number)
    # return the objects that satisfy all search filters
    return render(request, 'hits/hits.html', {"hits": hit_page})

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
    # api call - gets all qualifications created by admin
    try:
        qualifications = mturk.list_qualification_types(  
            MustBeRequestable=False,
            MustBeOwnedByCaller=True)
    except mturk.exceptions.ServiceFault:
        messages.error(request, "API Service Fault")
    except mturk.exceptions.RequestError:
        messages.error(request, "Unable to get qualification types")
    
    # retreive inactive qual types from db and cross reference with mturk api call (data check)
    qual_objects = Qualification.objects.filter(status='Inactive')
    for item in qual_objects:
        try:
            response = mturk.get_qualification_type(
                QualificationTypeId=item.QualificationTypeId)
        except mturk.exceptions.ServiceFault:
            messages.error(request, "API Service Fault")
        except mturk.exceptions.RequestError:
            messages.error(request, "Unable to get qualification types")
        qualifications['QualificationTypes'].append(response['QualificationType'])

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
    # paginate by 10
    paginator = Paginator(qualifications['QualificationTypes'], 10)
    page_number = request.GET.get('page')
    qualification_page = paginator.get_page(page_number)
    # return the objects that satisfy all search filters
    return render(request, 'qualifications/qualifications.html', {"qualifications": qualification_page})

# display add qualifiction form page
def addQualificationView(request):
    """
    Add a new qualification
    :param request
    :return: Redirect to Assignment View page after changes are made
    """
    # init list of qualification fields
    mturk = mturk_client()
    qual_fields = ['nickname', 'description', 'comparator', 'int_value', 'country', 'subdivision']  
    # init list of the required country field
    country_list = []
    for name in list(countries):
        country_list.append(name)
    if request.method == "POST":
        # qualification form
        form = QualificationForm(request.POST or None)
        if form.is_valid():
            # init field data list
            qual_info = []  
            for i in qual_fields:
                qual_info.append(form.cleaned_data[i])
            # api call - create qualification type
            try:
                response = mturk.create_qualification_type(  
                    Name= qual_info[0],
                    Description= qual_info[1],
                    QualificationTypeStatus='Active')
                # create qualification object and store on db
                new_qualification = Qualification(  
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
            # error handling for ServiceFault, RequestError
            except mturk.exceptions.ServiceFault:  
                messages.error(request, "API Service Fault. Please try again later")
            except mturk.exceptions.RequestError:
                messages.error(request, "Failed to create qualification type. Please try again.")
            except:
                messages.error(request, "Unexpected Error")
            return redirect(qualificationsView)
        else:
            messages.error(request, "Item was not added")
            return redirect(qualificationsView)
    else:
        context = {"country": country_list}
        return render(request, 'qualifications/addQualification.html', context)

# updating qualifications
def updateQualificationView(request, List_id):
    mturk = mturk_client()
    # retrieve the qualification in the database
    db_qual = Qualification.objects.get(QualificationTypeId=List_id)

    # cross reference with mturk with an api call (data integrity check)
    try:
        qual = mturk.get_qualification_type(QualificationTypeId=db_qual.QualificationTypeId)
    except mturk.exceptions.ServiceFault:
        messages.error(request, "API Service Fault")
    except mturk.exceptions.RequestError:
        messages.error(request, "Unable to update qualification")

    # update active/inactive status
    if qual['QualificationType']['QualificationTypeStatus'] == 'Inactive':
        try:
            # api call - update qualification type on mturk
            mturk.update_qualification_type(
                QualificationTypeId= List_id,
                QualificationTypeStatus='Active')
            # database - update qualification status on db
            db_qual.status = 'Active'
            db_qual.save()
        except mturk.exceptions.ServiceFault:
            messages.error(request, "API Service Fault")
        except mturk.exceptions.RequestError:
            messages.error(request, "Unable to update qualification")
    else:
        try:
            # api call - updates the qualification type
            mturk.update_qualification_type(
                QualificationTypeId= List_id,
                QualificationTypeStatus='Inactive')
            # database - update qualification status on db
            db_qual.status = 'Inactive'
            db_qual.save()
        except mturk.exceptions.ServiceFault:
            messages.error(request, "API Service Fault")
        except mturk.exceptions.RequestError:
            messages.error(request, "Unable to update qualification")

    messages.success(request, "Item has been Updated!")
    return redirect('qualifications')

# display workers table
def workersView(request):
    """
    Workers view Page
    :param request
    :return: Workers view page
    """
    mturk = mturk_client()
    workers_list = []
    hitID_list = []
    # retrieve all hit IDs
    for i in Hit.objects.all():  
        hitID_list.append(i.hit_id)
    # retrieve all assignments for that hit ID
    for id in hitID_list:
        # api call - retrieve all assignments based on hit ID
        try:
            response = mturk.list_assignments_for_hit(  
                HITId=id,
                AssignmentStatuses=['Submitted', 'Approved', 'Rejected'])
            for item in response['Assignments']:
                workers_list.append(item)
        # exception raised if hit id not found
        except mturk.exceptions.RequestError:  
            print("Could not retrieve", id)
        except mturk.exceptions.ServiceFault:
            messages.error(request, "API Service Fault")
    # paginate by 10
    paginator = Paginator(workers_list, 10)
    page_number = request.GET.get('page')
    worker_page = paginator.get_page(page_number)
    return render(request, 'workers/workers.html', {"workers": worker_page})

# assign qualifications to worker
def workerAssignQualView(request, worker_id):
    """
    Workers Assign qualifications view Page
    :param request, worker_id
    :return: Workers view page
    """
    mturk = mturk_client()
    # api call - gets all qualifications created by admin
    try:  
        qualifications_api = mturk.list_qualification_types(  
            MustBeRequestable=False,
            MustBeOwnedByCaller=True)
    except mturk.exceptions.ServiceFault:
        messages.error(request, "API Service Fault")
    except mturk.exceptions.RequestError:
        messages.error(request, "Unable to get qualification types")
    # api call - assign selected qual need to be in a loop
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

# display active assignments table
def asgmtsActiveView(request):
    """
    View Active assignment
    :param request
    :return: Active assignment page
    """   
    # retrieve all active assignment objects and sort
    activeassign_items = AssignStatModel.objects.all().order_by('-id')
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
    # select all active assignments accordingly
    activeassign_items = AssignStatModel.objects.all()
    activeassign_filtered = []
    for item in activeassign_items:
        if str(item.hit_id) in hits_filtered:
            activeassign_filtered.append(item)
    activeassign_items = activeassign_filtered
    # retrieve queries for all assignment fields
    if request.method == "POST":
        assign_id = request.POST.get('assign_id')   
        worker_id = request.POST.get('worker_id')   
        hit_id = request.POST.get('hit_id')                          
        flag = request.POST.get('flag')  
        # filter the objects according to the sort
        if assign_id != '' and assign_id is not None:
            activeassign_items = activeassign.filter(assign_id__icontains=assign_id)
        if worker_id != '' and worker_id is not None:
            activeassign_items = activeassign_items.filter(worker_id__icontains=worker_id)
        if hit_id != '' and hit_id is not None:
            activeassign_items = activeassign_items.filter(hit_id__icontains=hit_id)
        if flag != '' and flag is not None:
            activeassign_items = activeassign_items.filter(flag__icontains=flag)
    # paginate by 10
    paginator = Paginator(activeassign_items, 10)
    page_number = request.GET.get('page')
    assignment_page = paginator.get_page(page_number)
    # return the objects that satisfy all search filters
    return render(request, 'assignments/asgmtsActive.html', {"assignments": assignment_page})

# display completed assignments table 
def asgmtsCompletedView(request):
    """
    View Completed assignments
    :param request
    :return: Completed assignments page
    """
    mturk = mturk_client()
    # approve chosen assigments if approve button pressed
    if request.method == "POST" and request.POST.get("approve"):
        chosen_asgmts = request.POST.getlist('chosen_assignments')
        for assignmentId in chosen_asgmts:
            mturk.approve_assignment(AssignmentId=str(assignmentId))
    # reject chosen assigments if reject button pressed
    if request.method == "POST" and request.POST.get("reject"):
        chosen_asgmts = request.POST.getlist('chosen_assignments')
        for assignmentId in chosen_asgmts:
            mturk.reject_assignment(AssignmentId=str(assignmentId), RequesterFeedback="rejected")

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
    assignments = []
    for hit_id in hits_filtered:
        for assignment in mturk.list_assignments_for_hit(HITId=hit_id)['Assignments']:
            assignments.append(assignment)
    # sort assignments based on time submitted
    assignments.sort(key=lambda item:item['SubmitTime'], reverse=True)
    # append/create bonus information for assignments
    for assignment in assignments:
        bonus = Bonus.objects.filter(assignment_id=assignment['AssignmentId'])
        if bonus:
            assignment['Amount'] = bonus[0].amount
            assignment['BonusStatus'] = bonus[0].status
        else:
            amount = round(random.uniform(0.5,5.0),2)
            bonus_item = Bonus.objects.create(
                assignment_id=assignment['AssignmentId'], 
                worker_id=assignment['WorkerId'], 
                amount=amount, 
                status='Unpaid'
            )
            assignment['Amount'] = bonus_item.amount
            assignment['BonusStatus'] = bonus_item.status
    # retrieve queries for all assignment fields
    if request.method == "POST":
        assignmentIdFilter = request.POST.get('assignmentId')  
        workerIdFilter = request.POST.get('workerId')          
        acceptTimeFilter = request.POST.get('acceptanceTime')  
        submitTimeFilter = request.POST.get('submittedTime')   
        statusFilter = request.POST.get('status')
        bonusFilter = request.POST.get('bonus')                 
        # filter the objects according to the sort
        if assignmentIdFilter != '' and assignmentIdFilter is not None:
            temp_assignments = []
            for assignment in assignments:
                if assignmentIdFilter.lower() in assignment['AssignmentId'].lower():
                    temp_assignments.append(assignment)
            assignments = temp_assignments
        if workerIdFilter != '' and workerIdFilter is not None:
            temp_assignments = []
            for assignment in assignments:
                if  workerIdFilter.lower() in assignment['WorkerId'].lower():
                    temp_assignments.append(assignment)
            assignments = temp_assignments
        if acceptTimeFilter != '' and acceptTimeFilter is not None:
            temp_assignments = []
            for assignment in assignments:
                if acceptTimeFilter.lower() in assignment['AcceptTime'].strftime("%B %-d, %Y, %-H:%M %p").lower():
                    temp_assignments.append(assignment)
            assignments = temp_assignments
        if submitTimeFilter != '' and submitTimeFilter is not None:
            temp_assignments = []
            for assignment in assignments:
                if submitTimeFilter.lower() in assignment['SubmitTime'].strftime("%B %-d, %Y, %-H:%M %p").lower():
                    temp_assignments.append(assignment)
            assignments = temp_assignments
        if statusFilter != '' and statusFilter is not None:
            temp_assignments = []
            for assignment in assignments:
                if statusFilter.lower() in assignment['AssignmentStatus'].lower():
                    temp_assignments.append(assignment)
            assignments = temp_assignments
        if bonusFilter != '' and bonusFilter is not None:
            temp_assignments = []
            for assignment in assignments:
                if bonusFilter.lower() in assignment['BonusStatus'].lower():
                    temp_assignments.append(assignment)
            assignments = temp_assignments
    # paginate by 10
    paginator = Paginator(assignments, 10)
    page_number = request.GET.get('page')
    assignment_page = paginator.get_page(page_number)
    # return the objects that satisfy all search filters
    return render(request, 'assignments/asgmtsCompleted.html', {"assignments": assignment_page})

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
    # paginate by 10
    paginator = Paginator(lobby_list, 10)
    page_number = request.GET.get('page')
    lobby_page = paginator.get_page(page_number)
    return render(request, 'lobby/lobby.html', {"lobby": lobby_page,"total_users": total_users, "ready_users": ready_users})

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
    # paginate by 10
    paginator = Paginator(experiment_items, 10)
    page_number = request.GET.get('page')
    experiment_page = paginator.get_page(page_number)
    # return the objects that satisfy all search filters
    return render(request, 'experiments/experiments.html', {"experiments": experiment_page})

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


@xframe_options_exempt
def ticView(request , hit_id):
    player = request.GET.get ('worker_id')
    assign_id = request.GET.get('assign_id')
    number = AssignStatModel.objects.filter(worker_id = player)
    name =""
    for x in number:
        if x.flag == 1:
            name = 'X'
        else:
            name ='O'

    context = {"player": player , "hit_id":hit_id,"name":name , "assign_id":assign_id}
    return render(request, 'games/tic.html',context)

def deleteassign(request , worker_id):
    item = AssignStatModel.objects.get(worker_id = worker_id)
    item.delete()
    return redirect('../')

@xframe_options_exempt
def  please(request):
    hit_id = request.GET.get('hitId')
    worker_id = request.GET.get('workerId')
    assign_id = request.GET.get('assignmentId')
    flag = 0
    if assign_id:

        assignment = AssignStatModel.objects.create(assign_id=assign_id, hit_id=hit_id, worker_id=worker_id,flag = flag)
        assign = AssignStatModel.objects.filter(hit_id= hit_id)

        duplicates = AssignStatModel.objects.values('worker_id')
        duplicates = duplicates.order_by()
        duplicates = duplicates.annotate(
            min_id=models.Min("id"), count_id=models.Count("id")
        )
        duplicates = duplicates.filter(count_id__gt=1)

        for duplicate in duplicates:
            to_delete = AssignStatModel.objects.filter(worker_id=worker_id)
            to_delete = to_delete.exclude(id=duplicate["min_id"])
            to_delete.delete()

        if (assign.count() == 2):
            
            player = worker_id
            first_assign = AssignStatModel.objects.filter(hit_id=hit_id).first()
            first_assign.flag = 1
            first_assign.save()
    
            return redirect( '/tic/' + hit_id + '?worker_id=' + player + '&assign_id=' + assign_id )
        else:
            return render(request, 'games/please.html',{'worker_id': worker_id})

    else:
        messages.error(request,"Invalid Assignment ID")
        return render(request, 'games/please.html',{'worker_id':worker_id})
