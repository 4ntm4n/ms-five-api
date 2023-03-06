from django.urls import path
from . import views
from tasks.views import CreateGroupTaskView

urlpatterns = [
    path('groups/', views.GroupListView.as_view()),
    path('groups/<int:pk>/', views.GroupDetailView.as_view()),
    path('groups/<int:pk>/members/', views.GroupMembersView.as_view()),
    
    #view for creating a task for a specific group
    path('groups/<int:group_id>/task/create/', CreateGroupTaskView.as_view()),
]
