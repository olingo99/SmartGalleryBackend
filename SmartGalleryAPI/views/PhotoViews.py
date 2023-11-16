from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from ..models import Photo, Person
from ..serializers import PhotoSerializer, PersonSerializer
import deepface

class PhotoListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the photo items for given requested user
        '''
        photos = Photo.objects.filter(User = request.user.id)
        serializer = PhotoSerializer(photos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Photo with given photo data
        '''
        data = {
            'Path': request.data.get('Path'), 
            'Location': request.data.get('Location'), 
            'User': request.user.id
        }
        serializer = PhotoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

class PhotoDetailApiView(APIView):
        # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, photo_id, user_id):
        '''
        Helper method to get the object with given photo_id, and user_id
        '''
        try:
            return Photo.objects.get(pk=photo_id, User = user_id)
        except Photo.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request, photo_id, *args, **kwargs):
        '''
        Retrieves the Photo with given photo_id
        '''
        photo_instance = self.get_object(photo_id, request.user.id)
        if not photo_instance:
            return Response(
                {"res": "Object with photo id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = PhotoSerializer(photo_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, photo_id, *args, **kwargs):
        '''
        Updates the photo item with given photo_id if exists
        '''
        print("put")
        photo_instance = self.get_object(photo_id, request.user.id)
        if not photo_instance:
            return Response(
                {"res": "Object with photo id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'Path': request.data.get('Path'),
            'Location': request.data.get('Location'),
            'User': request.user.id,
            'Date': request.data.get('Date')
        }
        serializer = PhotoSerializer(instance = photo_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, photo_id, *args, **kwargs):
        '''
        Deletes the photo item with given photo_id if exists
        '''
        photo_instance = self.get_object(photo_id, request.user.id)
        if not photo_instance:
            return Response(
                {"res": "Object with photo id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        photo_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )



from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse

# class UploadFileForm(forms.Form):
#     file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

class testUploadPhoto(APIView):
    def post(self, request, *args, **kwargs):
        '''
        Create the Photos with given photo data
        '''
        print(request.method)
        print(request.FILES)
        a = request.FILES
        print(type(a))
        if 'file0' not in request.FILES:
            return Response({'error': 'No file for upload'}, status=400)
        for name, file in request.FILES.lists():
            # print(file[0].name)
            # print(file.name)
            # print(name)
            FileSystemStorage(location="C:/Users/engel/Documents/5MIN/SmartGalleryBackend/temp").save(file[0].name, file[0])
        print('success')
        return Response(status=200)
    # def post(self, request, *args, **kwargs):
    #     '''
    #     Create the Photos with given photo data
    #     '''
    #     print(request.method)
    #     form = UploadFileForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         for key in request.FILES.keys():
    #             in_memory_file_obj = request.FILES[key]
    #             FileSystemStorage(location="C:/Users/engel/Documents/5MIN/SmartGalleryBackend/temp").save(in_memory_file_obj.name, in_memory_file_obj)
    #         print('success')
    #         return Response(status=200)
    #     else:
    #         print(form.errors)
    #         form = UploadFileForm()
    #         print('not success')
    #         return Response(status=400)
    # def post(self, request, *args, **kwargs):
    #     '''
    #     Create the Photo with given photo data
    #     '''
    #     print(request.method)
    #     form = UploadFileForm(request.POST, request.FILES)
    #     if True:
    #         in_memory_file_obj = request.FILES["file"]
    #         FileSystemStorage(location="C:/Users/engel/Documents/5MIN/SmartGalleryBackend/temp").save(in_memory_file_obj.name, in_memory_file_obj)
    #         # return HttpResponseRedirect("/success/url/")
    #         print('succes')
    #         return Response(status=200)
    #     else:
    #         form = UploadFileForm()
    #     # return render(request, "upload.html", {"form": form})
    #         print('not succes')