from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from ..models import Person
from ..serializers import PersonSerializer



class PersonListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

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
        # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

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
        person_instance = self.get_object(person_id, request.user.id)
        if not person_instance:
            return Response(
                {'error': 'Person not found'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = PersonSerializer(person_instance, data=request.data)
        if serializer.is_valid():
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
    


