from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from ..models import Person, LinkPhotoPerson, Photo, CroppedFace
from ..serializers import PersonSerializer, LinkPhotoPersonSerializer
import os

class LinkPhotoPersonApiView(APIView):
    def put(self, request,LinkId, *args, **kwargs):
        '''
        Update the LinkPhotoPerson instance
        '''
        link_photo_person = LinkPhotoPerson.objects.get(id=LinkId)

        if link_photo_person.Photo.User != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)


        old_person_Id = link_photo_person.Person_id
        link_photo_person.Person_id = request.data['Person_id']
        link_photo_person.save()
        photoId = link_photo_person.Photo_id
        personId = request.data['Person_id']
        print('photoId', photoId)
        print('personId', personId)
        print('old_person_Id', old_person_Id)
        croppedface = CroppedFace.objects.get(Person_id=old_person_Id, OriginalPhoto_id=photoId)
        croppedface.Person_id = personId
        croppedface.save()
        croppedFaceNumber = len(CroppedFace.objects.filter(Person_id=personId))
        os.rename(croppedface.Path, 'faceDataBase/'+str(personId)+'/'+str(croppedFaceNumber)+'.png')
        if os.path.exists('faceDataBase/representations_vgg_face.pki'): 
            os.remove('faceDataBase/representations_vgg_face.pki') 
        return Response(status=status.HTTP_200_OK)