from django.urls import path

from .views.PhotoViews import (
    PhotoListApiView,
    PhotoDetailApiView,
    testUploadPhoto,
    AllPhotoListApiView,
    PhotoPersonAPIView,
)

from .views.PersonViews import (
    PersonListApiView,
    PersonDetailApiView,
)

from .views.PhotoPersonLinkViews import (
    LinkPhotoPersonApiView,
)

from .views.CroppedFaceView import (
    CroppedFaceApiView,
)

app_name = "SmartGalleryAPI"
urlpatterns = [
    path("PhotoApi",PhotoListApiView.as_view() ),
    path("PhotoApi/<int:photo_id>",PhotoDetailApiView.as_view() ),
    path("PersonApi",PersonListApiView.as_view() ),
    path("PersonApi/<int:person_id>",PersonDetailApiView.as_view() ),
    path("PhotoApi/upload", testUploadPhoto.as_view()),
    path("AllPhotoApi",AllPhotoListApiView.as_view() ),
    path("LinkPhotoPersonApi/<int:PhotoId>",LinkPhotoPersonApiView.as_view() ),
    path("PhotoPersonApi/<int:person_id>",PhotoPersonAPIView.as_view() ),
    path("CroppedFaceApi/<int:person_id>",CroppedFaceApiView.as_view() ),
]