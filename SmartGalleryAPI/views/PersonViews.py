from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from ..models import Person, LinkPhotoPerson
from ..serializers import PersonSerializer
import os




# deprecated, use link api to fuse all photos
# def fuse(old_person_instance, new_name):
#     '''
#     Fuses the given person with the person with given new_name
#     '''
#     # Get the person with given new_name
#     new_person_instance = Person.objects.get(Name=new_name)

#     link_photo_person_instances = LinkPhotoPerson.objects.filter(Person=old_person_instance)

#     # Change the person associated with each LinkPhotoPerson instance to the new person
#     for link_photo_person in link_photo_person_instances:
#         link_photo_person.Person = new_person_instance
#         link_photo_person.save()

#     # Move all cropped faces of the person to the new_person
#     person_cropped_faces = old_person_instance.croppedface_set.all()
#     nb_cropped_faces = len(new_person_instance.croppedface_set.all())
#     for cropped_face in person_cropped_faces:
#         cropped_face.Person = new_person_instance
#         new_path = 'faceDataBase/'+str(new_person_instance.id)+'/'+str(nb_cropped_faces)+'.png'
#         os.rename(cropped_face.Path, new_path)
#         cropped_face.Path = new_path
#         nb_cropped_faces += 1
#         cropped_face.save()
#     os.rmdir('faceDataBase/'+str(old_person_instance.id))
#     if os.path.exists('faceDataBase/representations_vgg_face.pki'): 
#         os.remove('faceDataBase/representations_vgg_face.pki')
#     # Delete the person
#     new_person_photos = new_person_instance.photo_set.all()
#     print('new_person_photos', new_person_photos)
#     old_person_instance.delete()



class PersonListApiView(APIView):
    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the Person items for given requested user
        '''
        photos = Person.objects.filter(User = request.user.id)
        serializer = PersonSerializer(photos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Person with given person data
        '''
        data = {
            'Name': request.data.get('Name'), 
            'User': request.user.id
        }
        serializer = PersonSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PersonDetailApiView(APIView):
    def get_object(self, person_id, user_id):
        '''
        Helper method to get the object with given person_id, and user_id
        '''
        try:
            return Person.objects.get(pk=person_id, User = user_id)
        except Person.DoesNotExist:
            return None
    
    # 3. Retrieve
    def get(self, request, person_id, *args, **kwargs):
        '''
        Retrieves the Person with given person_id
        '''
        person_instance = self.get_object(person_id, request.user.id)
        print('person_instance at get', person_instance)
        if not person_instance:
            return Response(
                {'error': 'Person not found'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = PersonSerializer(person_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, person_id, *args, **kwargs):
        '''
        Updates the Person with given person_id
        '''
        print(request.user)
        person_instance = self.get_object(person_id, request.user.id)
        if not person_instance:
            return Response(
                {'error': 'Person not found'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if the name has changed
        # new_name = request.data.get('Name')
        # if new_name and new_name != person_instance.Name:
        #     # Check if the new name already exists
        #     if Person.objects.filter(Name=new_name, User = request.user).exists():
        #         # Call the fuse function
        #         fuse(person_instance, new_name)
        #         return Response(
        #             {'success': 'Person fused successfully'},
        #             status=status.HTTP_200_OK
        #         )

        serializer = PersonSerializer(person_instance, data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            validated_data.pop('User', None)
            serializer.save()
            return Response(
                {'success': 'Person updated successfully'},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # 5. Delete
    def delete(self, request, person_id, *args, **kwargs):
        '''
        Deletes the Person with given person_id
        '''
        person_instance = self.get_object(person_id, request.user.id)
        if not person_instance:
            return Response(
                {'error': 'Person not found'},
                status=status.HTTP_400_BAD_REQUEST
            )
        person_instance.delete()
        return Response(
            {'success': 'Person deleted successfully'},
            status=status.HTTP_200_OK
        )
    


