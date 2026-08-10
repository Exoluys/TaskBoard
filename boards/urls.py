from django.urls import path

from boards.views import BoardListCreateApi, BoardDetailApi, BoardDetailSpecificApi

urlpatterns = [
    path("", BoardListCreateApi.as_view()),
    path("<int:pk>/", BoardDetailApi.as_view()),
    path("<int:pk>/details/", BoardDetailSpecificApi.as_view())
]