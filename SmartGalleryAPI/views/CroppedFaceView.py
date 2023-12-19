from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from ..models import CroppedFace
from ..serializers import CroppedFaceSerializer

class CroppedFaceApiView(APIView):
    def get(self, request, *args, **kwargs):
        '''
        Get all the CroppedFace instances
        '''
        croppedface = CroppedFace.objects.all()
        serializer = CroppedFaceSerializer(croppedface, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        '''
        Create a new CroppedFace instance
        '''
        serializer = CroppedFaceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)