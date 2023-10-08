from django.urls import path

from .views.PhotoViews import (
    PhotoListApiView,
    PhotoDetailApiView,
)

from .views.PersonViews import (
    PersonListApiView,
    PersonDetailApiView,
)

app_name = "SmartGalleryAPI"
urlpatterns = [
    path("PhotoApi",PhotoListApiView.as_view() ),
    path("PhotoApi/<int:photo_id>",PhotoDetailApiView.as_view() ),
    path("PersonApi",PersonListApiView.as_view() ),
    path("PersonApi/<int:person_id>",PersonDetailApiView.as_view() ),
]