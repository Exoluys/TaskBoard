from django.urls import path

from tasks.views import TaskListCreateApi, TaskDetailApi, TaskMoveApi

urlpatterns = [
    path("", TaskListCreateApi.as_view()),
    path("<int:pk>/", TaskDetailApi.as_view()),
    path("<int:pk>/move/", TaskMoveApi.as_view())
]