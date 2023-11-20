from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from ..models import Person, User
from ..serializers import PhotoSerializer, PersonSerializer

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


#maybe use middleware

# class CustomMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         response = self.get_response(request)
#         # Code to execute after the view goes here
#         print("This will be executed after the view")
#         return response

# need to add to middleware list
user = User.objects.get(pk=1)
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
        for _, file in request.FILES.lists():
            FileSystemStorage(location=f"temp").save(file[0].name, file[0])
            # print(list(os.walk(f"photos/{file[0].name}")))
            # photoObject = Photo.objects.create(Path=f"photos/{file[0].name}", User=user)
            # photoObject.save()
            detectSubject(f"temp/{file[0].name}")
        print('success')


        return Response(status=200)





import json
from ultralytics import YOLO
import os 
from deepface import DeepFace
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import os
from ..models import Person, CroppedFace, LinkPhotoPerson, Photo
from ..serializers import PersonSerializer, CroppedFaceSerializer

def detectSubject(img):
    model = YOLO("yolov8n.pt")
    # img = Image.open(img)
    res = model.predict(img)
    classes = []
    print(len(res))
    for result in res:
        print(len(result.boxes))
        for box in result.boxes:
            if box.cls == 0:
                return detectPerson(img)
            else:
                detectedClass = result.names[int(box.cls[0])]
                if  detectedClass not in classes : classes.append(detectedClass) 
    return ((),f"No human, {' '.join(str(i) for i in classes)} in image")




def detectPerson(img):
    faces = DeepFace.extract_faces(img, detector_backend='mtcnn')
    image = Image.open(img)
    # image = img
    size = image.size
    # print(size)
    padding_sacle = 0.05
    padding = (padding_sacle*size[0], padding_sacle*size[1])
    find_result = {}
    for face in faces:
        face = face['facial_area']
        x1,x2 = max(face['x']-padding[0],0), min(face['x']+face['w']+padding[0], size[0])
        y1,y2 = max(face['y']-padding[1],0), min(face['y']+face['h']+padding[1], size[1])
        cropped_face = image.crop((x1, y1, x2, y2))
        # cropped_face = numpy.array(cropped_face)
        cropped_face.save("temp/cropped_face.png")
        face_result = DeepFace.find("temp/cropped_face.png", "faceDataBase", enforce_detection=False)
        max_cosine = float('inf')
        max_index = -1

        for i, df in enumerate(face_result):
            cosine = df['VGG-Face_cosine'].min()
            if cosine < max_cosine:
                max_cosine = cosine
                max_index = i
        print('max_index', max_index)
        print('face_result', face_result)

        max_df = face_result[max_index]
        print(max_df)
        max_row = max_df.loc[max_df['VGG-Face_cosine'].idxmin()]
        print(max_row['identity'])
        print(max_row['VGG-Face_cosine'])
        if max_row['VGG-Face_cosine'] <= 0.2:                           #to do after new face is done
            identity = max_row['identity'].replace("\\", "/")
            identity = identity.split("/")[-2]
            print('identity ' + identity)
            find_result[len(find_result)]=(face,identity)
            os.remove("temp/cropped_face.png")
            photo = Photo.objects.create(Path=f"photos/{identity}.png", User=user)
            photo.save()
            # extension = os.path.splitext(img)[1]
            os.rename(img, f"photos/{identity}/{img.split('/')[-1]}")

            LinkPhotoPerson.objects.create(BoundingBox=f"{x1},{y1},{x2},{y2}", Person=Person.objects.get(pk=identity), Photo=photo).save()

        else:
            # id = len(find_result)
            person = Person.objects.create(Name='Unknown', User=user)
            person.save()
            id = person.id
            os.mkdir(f"faceDataBase/{person.id}")
            os.rename("temp/cropped_face.png", f"faceDataBase/{person.id}/0.png")
            # FileSystemStorage(location=f"photos/{person.id}").save(img, image)
            # extension = os.path.splitext(img)[1]
            os.mkdir(f"photos/{person.id}")
            os.rename(img, f"photos/{person.id}/{img.split('/')[-1]}")

            photoObject = Photo.objects.create(Path=f"photos/{person.id}/0.png", User=user, )
            photoObject.save()
            link = LinkPhotoPerson.objects.create(BoundingBox=f"{x1},{y1},{x2},{y2}", Person=person, Photo=photoObject)
            link.save()
            croppedFaceObject = CroppedFace.objects.create(Path=f"faceDataBase/{person.id}/0.png", Person=person, OriginalPhoto=photoObject)
            croppedFaceObject.save()

            os.remove("faceDataBase/representations_vgg_face.pkl")

            # id = len([name for name in os.listdir("temp/faceDataBase")])

            face_result = (face,"Unknown")
            find_result[id]=face_result
            # name = addToDb(cropped_face, id, face_result)
    return find_result
