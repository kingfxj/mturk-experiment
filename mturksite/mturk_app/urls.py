from django.urls import path
from . import views

urlpatterns = [
    path('', views.assignmentsListCreate.as_view() ),
]