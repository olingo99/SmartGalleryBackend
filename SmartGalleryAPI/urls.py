from django.urls import path

from .views import (
    PhotoListApiView
)

app_name = "SmartGalleryAPI"
urlpatterns = [
    path("api",PhotoListApiView.as_view() ),
]