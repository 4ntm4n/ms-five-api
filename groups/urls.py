from django.urls import path
from . import views

urlpatterns = [
    path('groups/', views.GroupListView.as_view()),
    path('groups/<int:pk>/', views.GroupDetailView.as_view()),
]
