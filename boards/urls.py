from django.urls import path

from boards.views import BoardListCreateApi, BoardDetailApi, BoardDetailSpecificApi, BoardMemberApi, \
    BoardMemberDetailApi

urlpatterns = [
    path("", BoardListCreateApi.as_view()),
    path("<int:pk>/", BoardDetailApi.as_view()),
    path("<int:pk>/details/", BoardDetailSpecificApi.as_view()),
    path("<int:board>/members/", BoardMemberApi.as_view()),
    path("<int:board>/members/<int:pk>/", BoardMemberDetailApi.as_view()),
]