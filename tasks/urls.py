from django.urls import path
from . import views

urlpatterns = [
    path('tasks/', views.TaskListView.as_view()),
    path('tasks/<int:pk>', views.TaskListView.as_view()),
]
