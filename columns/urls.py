from django.urls import path

from columns.views import ColumnListCreateApi, ColumnDetailApi, ColumnDetailSpecificApi, ColumnMoveApi

urlpatterns = [
    path("", ColumnListCreateApi.as_view()),
    path("<int:pk>/", ColumnDetailApi.as_view()),
    path("<int:pk>/details/", ColumnDetailSpecificApi.as_view()),
    path("<int:pk>/move/", ColumnMoveApi.as_view())
]