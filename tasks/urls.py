from django.urls import path
from . import views

urlpatterns = [
    path('tasks/', views.TaskListView.as_view()),
    path('tasks/<int:pk>', views.TaskListView.as_view()),
    #path('tasks/events/', views.TaskEventListView.as_view()),
    #path('groups/<int:pk>/tasks/', views.GroupTaskListView.as_view())
]
