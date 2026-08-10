from django.urls import path

from columns.views import ColumnListCreateApi, ColumnDetailApi, ColumnDetailSpecificApi

urlpatterns = [
    path("", ColumnListCreateApi.as_view()),
    path("<int:pk>/", ColumnDetailApi.as_view()),
    path("<int:pk>/details/", ColumnDetailSpecificApi.as_view())
]