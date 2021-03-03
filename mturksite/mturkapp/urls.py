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

urlpatterns = [
    path('', views.assignmentView, name="assignmentView"),
    path('add/', views.addAssignment, name="addAssignment"),
    path('edit/<list_id>', views.editAssignment, name="editAssignment"),
    path('delete/<list_id>', views.deleteAssignment, name="deleteAssignment"),
    path('maintenance/', views.maintenanceView, name="maintenanceView"),
    path('management/', views.userManagementView, name="userManagementView"),
    path('lobby/', views.lobbyView, name="lobbyView"),
    path('hits/', views.hitView, name="hitView"),
]
