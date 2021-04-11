from django.test import TestCase
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
import json
import uuid
from mturkapp.models import Hit, Hittype, Qualification, Experiment
from mturkapp.mturk_client import mturk_client


class SignupViewTests(TestCase):

    def test_signupView_Health(self):
        response = self.client.get(reverse('signup'))
        # test OK
        self.assertEquals(response.status_code, 200)
        # test right template used
        self.assertTemplateUsed(response, 'registration/signup.html')

    def test_signupView_POST(self):
        response = self.client.post(reverse('signup'), {
            'username': 'test',
            'email': 'test@test.com',
            'password1': 'testpassword1234',
            'password2': 'testpassword1234'
        })
        # test redirect to 'login' works
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/')
        users = get_user_model().objects.all()
        # test user is saved to DB (should be single user in test DB)
        self.assertEqual(users.count(), 1)
        self.assertEqual(users[0].username, 'test')


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
            batch_id = 'test1234',
            batch_title = 'test1',
            title = 'test title 1',
            hittype_id = 'dsadsa',
            description = 'fake description1',
            keyword = 'test1',
            reward = '0.01',
            qualifications = 'testqual1'
        )
        
        hittype1 = Hittype.objects.create(
            batch_id = 'test8765',
            batch_title = 'test2',
            title = 'test title 2',
            hittype_id = 'fakeid2',
            description = 'fake description2',
            keyword = 'test2',
            reward = '1.00',
            qualifications = 'testqual2'
        )
        response = self.client.post(reverse('hittypes'), {
            'hittype_id':'fakeid2',
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

    def test_addQualificaitonDB(self):
        mturk = mturk_client()
        #test api call
        response = mturk.create_qualification_type(
            Name= 'testing_qual',
            Description= 'testing_qual_desc',
            QualificationTypeStatus='Active'
        )
        self.assertEqual(response['QualificationType']['Name'], 'testing_qual')
        new_qualification = Qualification(  
            nickname = response['QualificationType']['Name'],
            description = response['QualificationType']['Description'],
            QualificationTypeId = response['QualificationType']['QualificationTypeId'],
            comparator = '',
            int_value = '',
            country = '',
            subdivision = '',
            status = response['QualificationType']['QualificationTypeStatus'])
        new_qualification.save()

class WorkersViewTests(TestCase):

    def test_workersView_Health(self):
        response = self.client.get(reverse('workers'))
        # test OK
        self.assertEquals(response.status_code, 200)
        # test right template used
        self.assertTemplateUsed(response, 'workers/workers.html')


class AsgmtsActiveViewTests(TestCase):

    def test_asgmtsActiveView_Health(self):
        response = self.client.get(reverse('asgmtsActive'))
        # test OK
        self.assertEquals(response.status_code, 200)
        # test right template used
        self.assertTemplateUsed(response, 'assignments/asgmtsActive.html')


class AsgmtsCompletedViewTests(TestCase):

    def test_asgmtsCompletedView_Health(self):
        response = self.client.get(reverse('asgmtsCompleted'))
        # test OK
        self.assertEquals(response.status_code, 200)
        # test right template used
        self.assertTemplateUsed(response, 'assignments/asgmtsCompleted.html')


class LobbyViewTests(TestCase):

    def test_lobbyView_Health(self):
        response = self.client.get(reverse('lobby'))
        # test OK
        self.assertEquals(response.status_code, 200)
        # test right template used
        self.assertTemplateUsed(response, 'lobby/lobby.html')


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