from django.urls import path

from tasks.views import TaskListCreateApi, TaskDetailApi

urlpatterns = [
    path("", TaskListCreateApi.as_view()),
    path("<int:pk>/", TaskDetailApi.as_view()),
]