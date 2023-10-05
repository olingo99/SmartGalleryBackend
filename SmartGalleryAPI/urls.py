from django.urls import path

from .views import (
    PhotoListApiView,
    PhotoDetailApiView,
    PersonApiView,
)

app_name = "SmartGalleryAPI"
urlpatterns = [
    path("PhotoApi",PhotoListApiView.as_view() ),
    path("PhotoApi/<int:photo_id>",PhotoDetailApiView.as_view() ),
    path("PersonApi",PersonApiView.as_view() ),
]