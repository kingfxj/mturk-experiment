from django.test import TestCase
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
import json
import uuid
from mturkapp.models import Hit, Hittype, Qualification, Experiment ,  AssignStatModel
from mturkapp.mturk_client import mturk_client
from django.conf import settings
from faker import Faker
from nose.tools import nottest


#testing game and consumer
import asyncio
from urllib.parse import unquote

import pytest
from django.urls import path

from channels.consumer import AsyncConsumer
from channels.generic.websocket import WebsocketConsumer
from channels.routing import URLRouter
from channels.testing import HttpCommunicator, WebsocketCommunicator

from djangochannelsrestframework.decorators import action
from djangochannelsrestframework.consumers import AsyncAPIConsumer


'''
class LoginTests(TestCase):

    def test_login_health(self):
        response = self.client.get(reverse('login'))
        # test OK
        self.assertEquals(response.status_code, 200)
        # test right template used
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_login_Works(self):
        user = User.objects.create(username='test')
        user.set_password('testpassword1234')
        user.save()

        response = self.client.post(reverse('login'), {
            'username': 'test',
            'password': 'testpassword1234',
        })
        # test login successful and redirect to 'home' works
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')
        # test user is logged in and authenticated
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)


class HomeViewTests(TestCase):

    def test_homeView_Health(self):
        response = self.client.get(reverse('home'))
        # test OK
        self.assertEquals(response.status_code, 200)
        # test right template used
        self.assertTemplateUsed(response, 'home.html')


class HittypeViewTests(TestCase):

    def test_hittypeView_Health(self):
        response = self.client.get(reverse('hittypes'))
        # test OK
        self.assertEquals(response.status_code, 200)
        # test right template used
        self.assertTemplateUsed(response, 'hittypes/hittypes.html')

    def test_hittypeView_POST_filter(self):
        hittype1 = Hittype.objects.create(
            batch_id = '4251b7d5-bc0a-4f08-bd4f-65168e5a5163',
            batch_title = 'Testing',
            title = 'test title 1',
            hittype_id = 'dsadsa',
            description = 'fake description1',
            keyword = 'test1',
            reward = '0.01',
            qualifications = 'testqual1'
        )
        
        hittype2 = Hittype.objects.create(
            batch_id = '4251b7d5-bc0a-4f08-bd4f-65168e5a5163',
            batch_title = 'Testing',
            title = 'test title 2',
            hittype_id = 'fakeid2',
            description = 'fake description2',
            keyword = 'test2',
            reward = '1.00',
            qualifications = 'testqual2'
        )
        response = self.client.post(reverse('hittypes'), {
            'hittype_id': 'fakeid2'
        })

        # test OK
        self.assertEquals(response.status_code, 200)
        # I dont even think this test does anything, but I'm leaving it
        self.assertTrue(response.content)


class AddHittypeViewTests(TestCase):

    def test_addHittypeView_Health(self):
        response = self.client.get(reverse('addHittype'))
        # test OK
        self.assertEquals(response.status_code, 200)
        # test right template used
        self.assertTemplateUsed(response, 'hittypes/addHittype.html')

    def test_addHittypeView_POST_and_DB(self):
        batch = Experiment.objects.create(
            batch_id= '1ba05d73-0f19-4aa6-9195-037ed2391752',         # Random UUID 4 generated online 
            title='fake batch'
        )
        test = Experiment.objects.all()
        response = self.client.post(reverse('addHittype'),{
            'batch': test[0].batch_id,  # single entry in the database
            'title': 'fake title',
            'description': 'fake description',
            'keyword': 'fake',
            'reward': '0.01',
            'qualifications':'fake qual',
            'Assignment_Duration_In_Seconds': 600,
            'Auto_Approval_Delay_In_Seconds':600
        })
        # test if it redirects to hittypeView
        self.assertEqual(response.status_code, 302)
        #test if it is saved in the db(only single User in DB) 
        hittype_items = Hittype.objects.all()
        self.assertEqual(hittype_items.count(),1) 
        self.assertEqual(hittype_items[0].title , 'fake title')

    def test_addHittpeView_APICall(self):
        mturk = mturk_client()
        response = mturk.create_hit_type(
                        AutoApprovalDelayInSeconds = 600,
                        AssignmentDurationInSeconds = 600 ,
                        Reward = '0.01',
                        Title = 'fake hittype',
                        Keywords = 'testing',
                        Description = 'doing testing'
                    )

        # test create_hit_with_hit_type api call (As the response from the api is a dictionary)
        self.assertEqual(len(response["HITTypeId"]) , 30 )      # Checked that the count of every HITType ID is 30
    
class HitsViewTests(TestCase):

    def test_hitsView_Health(self):
        response = self.client.get(reverse('hits'))
        # test OK
        self.assertEquals(response.status_code, 200)
        # test right template used
        self.assertTemplateUsed(response, 'hits/hits.html')


class AddHitViewTests(TestCase):

    def test_addHitView_Health(self):
        response = self.client.get(reverse('addHit'))
        # test OK
        self.assertEquals(response.status_code, 200)
        # test right template used
        self.assertTemplateUsed(response, 'hits/addHit.html')

    def test_addHitView_POST_and_DB(self):
        mturk = mturk_client()
        addhit = Hittype.objects.create(
            batch_id = 'test8765',
            batch_title = 'test2',
            title = 'test title 2',
            hittype_id = '3CS3U1VE5KBFL43TLU25PEJOXNXS0M',
            description = 'fake description2',
            keyword = 'test2',
            reward = '1.00',
            qualifications = 'testqual2'
        )
        response = self.client.post(reverse('addHit'),{
            'hittype' : 1,
            'max_assignments':12,
            'lifetime_in_seconds':600
        })
        # test if it redirects to hitView
        self.assertEqual(response.status_code , 302)
        #test if it is saved in the db(only single User in DB)
        hit_items = Hit.objects.all()
        self.assertEqual(hit_items.count(),1)
        self.assertEqual(hit_items[0].hittype_id,'3CS3U1VE5KBFL43TLU25PEJOXNXS0M')

    def test_addHitView_APICall(self):
        mturk = mturk_client()
        test_game = str(settings.BASE_DIR) + "/mturkapp/templates/games/question.xml"
        question = open(test_game).read()
        response = mturk.create_hit_with_hit_type(
                HITTypeId = '3CS3U1VE5KBFL43TLU25PEJOXNXS0M',   # single hittype in the DB
                MaxAssignments = 12 ,
                LifetimeInSeconds= 600,
                Question =question
            )
        # test create_hit_with_hit_type api call (As the response from the api is a dictionary)
        self.assertEqual(response['HIT']['HITTypeId'] , '3CS3U1VE5KBFL43TLU25PEJOXNXS0M')

class QualificationsViewTests(TestCase):

    def test_qualificationsView_Health(self):
        response = self.client.get(reverse('qualifications'))
        # test OK
        self.assertEquals(response.status_code, 200)
        # test right template used
        self.assertTemplateUsed(response, 'qualifications/qualifications.html')



class AddQualificationViewTests(TestCase):

    def test_addQualificationView_Health(self):
        response = self.client.get(reverse('addQualification'))
        # test OK
        self.assertEquals(response.status_code, 200)
        # test right template used
        self.assertTemplateUsed(response, 'qualifications/addQualification.html')

    def test_addQualificaiton_APICall(self):
        mturk = mturk_client()
        self.fake = Faker()
        name = self.fake.name()    # To get random unique name for testing api call  

        response = mturk.create_qualification_type(
            Name= name,
            Description= 'testing_qual_desc',
            QualificationTypeStatus='Active'
        )

        # test for the api call  create_qualification_type
        self.assertEqual(response['QualificationType']['Name'], name)

    def test_addQualificationView_POST_and_DB(self):
        self.fake = Faker()
        name = self.fake.name()
        response = self.client.post(reverse('addQualification'), {
            'nickname':name,
            'description':'fake-description',
            'comparator':'EqualTo',
            'int_value':12,
            'country':''
        })
        # test if it redirects to qualificationsView
        self.assertEqual(response.status_code , 302)
        # test for database as there is a single entry in the database
        qualification = Qualification.objects.all()
        self.assertEqual(qualification.count(),1)   
        self.assertEqual(qualification[0].nickname,name)

class WorkersViewTests(TestCase):

    def test_workersView_Health(self):
        response = self.client.get(reverse('workersView'))
        # test OK
        self.assertEquals(response.status_code, 200)
        # test right template used
        self.assertTemplateUsed(response, 'workers/workers.html')
    
    def test_workersView_APICall(self):
        mturk = mturk_client()
        response = mturk.list_assignments_for_hit(  
                        HITId='3YO4AH2FPD7KJWGXZX8KAYBXYGXQ0U',                    # Use a HITId which you have worked/submitted on in Mturk Workersandbox
                        AssignmentStatuses=['Submitted', 'Approved', 'Rejected']
                    )

        #Test api call for displaying worker
        self.assertEqual(response['Assignments'][0]['HITId'] , '3YO4AH2FPD7KJWGXZX8KAYBXYGXQ0U')    # 2 assignments as 2 player played the game


class AsgmtsActiveViewTests(TestCase):

    def test_asgmtsActiveView_Health(self):
        response = self.client.get(reverse('asgmtsActive'))
        # test OK
        self.assertEquals(response.status_code, 200)
        # test right template used
        self.assertTemplateUsed(response, 'assignments/asgmtsActive.html')
    
    def test_asgmtsActiveView_POST(self):
        active_assignment = AssignStatModel.objects.create(
            hit_id= '3HXCEECSQMGQUJD9U126TJHLFVZYZX',
            worker_id='ARZFD8B9ETXJ4',
            assign_id= '4EIJUJFEOK20KGLMG0I565M30HFZZP',
            flag= 0
        )

        response = self.client.post(reverse('asgmtsActive'),{
            'hit_id':'3HXCEECSQMGQUJD9U126TJHLFVZYZX',
            'worker_id':'ARZFD8B9ETXJ4',
            'assign_id':'4EIJUJFEOK20KGLMG0I565M30HFZZP'
        })
        # Test that it shows active assignment
        self.assertEqual(response.status_code , 200)
class AsgmtsCompletedViewTests(TestCase):

    def test_asgmtsCompletedView_Health(self):
        response = self.client.get(reverse('asgmtsCompleted'))
        # test OK
        self.assertEquals(response.status_code, 200)
        # test right template used
        self.assertTemplateUsed(response, 'assignments/asgmtsCompleted.html')
        
        
class ExperimentsViewTests(TestCase):

    def test_experimentsView_Health(self):
        response = self.client.get(reverse('experiments'))
        # test OK
        self.assertEquals(response.status_code, 200)
        # test right template used
        self.assertTemplateUsed(response, 'experiments/experiments.html')


class AddExperimentViewTests(TestCase):

    def test_addExperimentView_Health(self):
        response = self.client.get(reverse('addExperiment'))
        # test OK
        self.assertEquals(response.status_code, 200)
        # test right template used
        self.assertTemplateUsed(response, 'experiments/addExperiment.html')


class ExperimentFilterViewTests(TestCase):

    def test_experimentFilterView_Health(self):
        response = self.client.get(reverse('experimentFilter'))
        # test OK
        self.assertEquals(response.status_code, 200)
        # test right template used
        self.assertTemplateUsed(response, 'experiments/experimentFilter.html')

'''


#testing game
class SimpleHttpApp(AsyncConsumer):
    """
    HTTP ASGI app for testing.
    """

    async def http_request(self, event):
        assert self.scope["path"] == "/test/"
        assert self.scope["method"] == "GET"
        assert self.scope["query_string"] == b"foo=bar"
        await self.send({"type": "http.response.start", "status": 200, "headers": []})
        await self.send({"type": "http.response.body", "body": b"test response"})


@pytest.mark.asyncio
async def test_http_communicator():
    """
    Tests that the HTTP communicator class works at a basic level.
    """
    communicator = HttpCommunicator(SimpleHttpApp(), "GET", "/test/?foo=bar")
    response = await communicator.get_response()
    assert response["body"] == b"test response"
    assert response["status"] == 200


class SimpleWebsocketApp(WebsocketConsumer):
    """
    WebSocket ASGI app for testing.
    """

    def connect(self):
        assert self.scope["path"] == "/testws/"
        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        self.send(text_data=text_data, bytes_data=bytes_data)


class ErrorWebsocketApp(WebsocketConsumer):
    """
    Barebones WebSocket ASGI app for error testing.
    """

    def receive(self, text_data=None, bytes_data=None):
        pass


class KwargsWebSocketApp(WebsocketConsumer):
    """
    WebSocket ASGI app used for testing the kwargs arguments in the url_route.
    """

    def connect(self):
        self.accept()
        self.send(text_data=self.scope["url_route"]["kwargs"]["message"])


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_websocket_communicator():
    """
    Tests that the WebSocket communicator class works at a basic level.
    """
    communicator = WebsocketCommunicator(SimpleWebsocketApp(), "/testws/")
    # Test connection
    connected, subprotocol = await communicator.connect()
    assert connected
    assert subprotocol is None
    # Test sending text
    await communicator.send_to(text_data="hello")
    response = await communicator.receive_from()
    assert response == "hello"
    # Test sending bytes
    await communicator.send_to(bytes_data=b"w\0\0\0")
    response = await communicator.receive_from()
    assert response == b"w\0\0\0"
    # Test sending JSON
    await communicator.send_json_to({"hello": "world"})
    response = await communicator.receive_json_from()
    assert response == {"hello": "world"}
    # Close out
    await communicator.disconnect()


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_websocket_application():
    """
    Tests that the WebSocket communicator class works with the
    URLRoute application.
    """
    application = URLRouter([path("testws/<str:message>/", KwargsWebSocketApp())])
    communicator = WebsocketCommunicator(application, "/testws/test/")
    connected, subprotocol = await communicator.connect()
    # Test connection
    assert connected
    assert subprotocol is None
    message = await communicator.receive_from()
    assert message == "test"
    await communicator.disconnect()


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_timeout_disconnect():
    """
    Tests that disconnect() still works after a timeout.
    """
    communicator = WebsocketCommunicator(ErrorWebsocketApp(), "/testws/")
    # Test connection
    connected, subprotocol = await communicator.connect()
    assert connected
    assert subprotocol is None
    # Test sending text (will error internally)
    await communicator.send_to(text_data="hello")
    with pytest.raises(asyncio.TimeoutError):
        await communicator.receive_from()
    # Close out
    await communicator.disconnect()


class ConnectionScopeValidator(WebsocketConsumer):
    """
    Tests ASGI specification for the connection scope.
    """

    def connect(self):
        assert self.scope["type"] == "websocket"
        # check if path is a unicode string
        assert isinstance(self.scope["path"], str)
        # check if path has percent escapes decoded
        assert self.scope["path"] == unquote(self.scope["path"])
        # check if query_string is a bytes sequence
        assert isinstance(self.scope["query_string"], bytes)
        self.accept()


paths = [
    "user:pass@example.com:8080/p/a/t/h?query=string#hash",
    "wss://user:pass@example.com:8080/p/a/t/h?query=string#hash",
    (
        "ws://www.example.com/%E9%A6%96%E9%A1%B5/index.php?"
        "foo=%E9%A6%96%E9%A1%B5&spam=eggs"
    ),
]



@pytest.mark.django_db
@pytest.mark.asyncio
@pytest.mark.parametrize("path", paths)
async def test_connection_scope(path):
    """
    Tests ASGI specification for the the connection scope.
    """
    communicator = WebsocketCommunicator(ConnectionScopeValidator(), path)
    connected, _ = await communicator.connect()
    assert connected
    await communicator.disconnect()


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_decorator():

    results = {}

    class AConsumer(AsyncAPIConsumer):
        @action()
        async def test_async_action(self, pk=None, **kwargs):
            results["test_action"] = pk
            return {"pk": pk}, 200

        @action()
        def test_sync_action(self, pk=None, **kwargs):
            results["test_sync_action"] = pk
            return {"pk": pk, "sync": True}, 200

    # Test a normal connection
    communicator = WebsocketCommunicator(AConsumer(), "/testws/")

    connected, _ = await communicator.connect()

    assert connected

    await communicator.send_json_to(
        {"action": "test_async_action", "pk": 2, "request_id": 1}
    )

    response = await communicator.receive_json_from()

    assert response == {
        "errors": [],
        "data": {"pk": 2},
        "action": "test_async_action",
        "response_status": 200,
        "request_id": 1,
    }

    await communicator.send_json_to(
        {"action": "test_sync_action", "pk": 3, "request_id": 10}
    )

    response = await communicator.receive_json_from()

    assert response == {
        "errors": [],
        "data": {"pk": 3, "sync": True},
        "action": "test_sync_action",
        "response_status": 200,
        "request_id": 10,
    }

    await communicator.disconnect()
