"""mturksite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from . import views
from django.urls import path
from js_urls.views import JsUrlsView

urlpatterns = [
    path('', views.homeView, name='home'),
    path('hittypes/', views.hittypesView, name="hittypes"),
    path('hittypes/addhittype/', views.addHittypeView, name="addHittype"),
    path('hits/', views.hitsView, name="hits"),
    path('hits/addhit/', views.addHitView, name="addHit"),
    path('qualification/', views.qualificationsView, name="qualifications"),
    path('qualification/addQualifications/', views.addQualificationView, name='addQualification'),
    path('qualification/updateQualification/<List_id>' , views.updateQualificationView , name = 'updateQualification'),
    path('workers/', views.workersView, name="workersView"),
    path('workers/workerAssignQualifications/<worker_id>' , views.workerAssignQualView , name = 'workerAssignQualView'),
    path('assignments/active/', views.asgmtsActiveView, name='asgmtsActive'),
    path('assignments/completed/', views.asgmtsCompletedView, name='asgmtsCompleted'),
    path('assignments/completed/pay_bonuses/', views.payBonusView, name='payBonuses'),
    path('experiments/', views.experimentsView, name="experiments"),
    path('experiments/addexperiment/', views.addExperimentView, name="addExperiment"),
    path('experiments/filter/', views.experimentFilterView, name="experimentFilter"),
    path('waitPage/', views.waitPageView, name='waitPage'),
    path('game/<hit_id>', views.gameView, name='game'),
   
]
