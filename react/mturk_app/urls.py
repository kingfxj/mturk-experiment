from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.assignmentsListCreate.as_view() ),
]