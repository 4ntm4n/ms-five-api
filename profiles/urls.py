from django.urls import path, include
from . import views

urlpatterns = [
    path('profiles/', views.ProfileListView.as_view()),
    path('profiles/<int:pk>/', views.ProfileDetailView.as_view()),

]
