from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from ..models import CroppedFace
from ..serializers import CroppedFaceSerializer

class CroppedFaceApiView(APIView):
    def get(self, request, person_id,  *args, **kwargs):
        '''
        Get the first CroppedFace instance associated with the Person
        '''
        croppedface = CroppedFace.objects.filter(Person=person_id).first()
        if croppedface is not None:
            serializer = CroppedFaceSerializer(croppedface)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "No CroppedFace found for this person"}, status=status.HTTP_404_NOT_FOUND)
