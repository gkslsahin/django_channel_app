from django.urls import include, path
from . import views

urlpatterns = [
    path("channels/", views.ModelViewSet.as_view(),name="channel"),
]