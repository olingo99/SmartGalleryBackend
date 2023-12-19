from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from ..models import Person, LinkPhotoPerson, Photo, CroppedFace
from ..serializers import PersonSerializer, LinkPhotoPersonSerializer
import os

class LinkPhotoPersonApiView(APIView):
    def put(self, request,PhotoId, *args, **kwargs):
        '''
        Update the LinkPhotoPerson instance
        '''
        old_person_Id = request.data['Old_Person_id']
        link_photo_person = LinkPhotoPerson.objects.get(Photo_id=PhotoId, Person_id=old_person_Id)
        # link_photo_person = LinkPhotoPerson.objects.get(id=LinkId)

        if link_photo_person.Photo.User != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)


        # old_person_Id = link_photo_person.Person_id
        link_photo_person.Person_id = request.data['New_Person_id']
        link_photo_person.save()
        photoId = link_photo_person.Photo_id
        personId = request.data['New_Person_id']
        print('photoId', photoId)
        print('personId', personId)
        print('old_person_Id', old_person_Id)
        croppedface = CroppedFace.objects.get(Person_id=old_person_Id, OriginalPhoto_id=photoId)
        croppedface.Person_id = personId
        croppedface.save()
        croppedFaceNumber = len(CroppedFace.objects.filter(Person_id=personId))
        os.rename(croppedface.Path, 'faceDataBase/'+str(personId)+'/'+str(croppedFaceNumber)+'.png')
        croppedface.Path = 'faceDataBase/'+str(personId)+'/'+str(croppedFaceNumber)+'.png'
        croppedface.save()
        nb_photos_old_person = len(LinkPhotoPerson.objects.filter(Person_id=old_person_Id))
        if nb_photos_old_person == 0:
            os.rmdir('faceDataBase/'+str(old_person_Id))
            try:
                old_person = Person.objects.get(id=old_person_Id)
                old_person.delete()
            except Person.DoesNotExist:
                pass
        if os.path.exists('faceDataBase/representations_vgg_face.pki'): 
            os.remove('faceDataBase/representations_vgg_face.pki') 
        return Response(status=status.HTTP_200_OK)