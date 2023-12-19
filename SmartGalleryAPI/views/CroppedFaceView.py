from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from ..models import CroppedFace
from ..serializers import CroppedFaceSerializer


from django.http import FileResponse
from django.conf import settings
import os

class CroppedFaceApiView(APIView):
    def get(self, request, person_id,  *args, **kwargs):
        '''
        Get the first CroppedFace instance associated with the Person
        '''
        croppedface = CroppedFace.objects.filter(Person=person_id).first()
        if croppedface is not None:
            # print(os.getcwd())
            wd = os.getcwd().replace('\\', '/')
            return FileResponse(open(f"{wd}/{croppedface.Path}", 'rb'), content_type='image/jpeg')
            # return FileResponse(open("C:/Users/engel/Documents/5MIN/SmartGalleryBackend/faceDataBase/133302/2.png", 'rb'), content_type='image/jpeg')

        else:
            return Response({"detail": "No CroppedFace found for this person"}, status=status.HTTP_404_NOT_FOUND)
    