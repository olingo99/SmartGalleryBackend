from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import PhotoSerializer
from django.db.models import Q
from ultralytics import YOLO
import os 
from deepface import DeepFace
from PIL import Image
from ..models import Person, CroppedFace, LinkPhotoPerson, Photo
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import re
from unidecode import unidecode

class PhotoTagGetApiView(APIView):
    def get(self, request, *args, **kwargs):
        '''
        List all the photo items for given requested user
        '''
        tag_string = self.request.query_params.get('Tag', None)
        if tag_string is None:
            return Response({"error":"No tag provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        photos = Photo.objects.filter(Q(User = request.user.id) & Q(Tag__icontains=tag_string))
        serializer = PhotoSerializer(photos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
class AllPhotoListApiView(APIView):
    def get(self, request, *args, **kwargs):
        '''
        List all the photo items for given requested user
        '''
        photos = Photo.objects.all()
        serializer = PhotoSerializer(photos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PhotoListApiView(APIView):

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the photo items for given requested user
        '''
        photos = Photo.objects.filter(User = request.user.id)
        serializer = PhotoSerializer(photos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PhotoPersonAPIView(APIView):
    def get(self, request, person_id, *args, **kwargs):
        '''
        List all the photo items for given requested user
        '''
        person = Person.objects.get(id=person_id)
        photos = person.photo_set.filter(User = request.user.id)
        serializer = PhotoSerializer(photos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PhotoDetailApiView(APIView):

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
        # print(request.user.id)
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
            'Path': request.data.get('Path', photo_instance.Path),
            'User': request.user.id,
            'Date': request.data.get('Date', photo_instance.Date),
            'Tag': request.data.get('Tag', photo_instance.Tag),
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




def clean_filename(filename):
    filename = unidecode(filename)
    filename = re.sub(r'[^a-zA-Z0-9_.-]', '', filename)
    return filename

# user = User.objects.get(pk=1)
class testUploadPhoto(APIView):
    def post(self, request, *args, **kwargs):
        '''
        Create the Photos with given photo data
        '''
        a = request.FILES
        if 'file0' not in request.FILES:
            return Response({'error': 'No file for upload'}, status=400)
        for _, file in request.FILES.lists():
            filename = clean_filename(file[0].name)
            filename = FileSystemStorage(location=f"temp").save(filename, file[0])
            detectSubject(f"temp/{filename}", request.user)
        print('success')


        return Response(status=200)





def detectSubject(img, user):
    model = YOLO("yolov8n.pt")
    res = model.predict(img)
    classes = []
    for result in res:
        for box in result.boxes:
            if box.cls == 0:
                return detectPerson(img, user)
            else:
                detectedClass = result.names[int(box.cls[0])]
                if  detectedClass not in classes : classes.append(detectedClass)
                person = Person.objects.get(Name=detectedClass) if detectedClass in Person.objects.values_list('Name', flat=True) else Person.objects.create(Name=detectedClass, User=user)
                person.save()    
                photo = Photo.objects.create(Path=f"photos/{img.split('/')[-1]}", User=user) if not Photo.objects.filter(Path=f"photos/{img.split('/')[-1]}").exists() else Photo.objects.get(Path=f"photos/{img.split('/')[-1]}")
                photo.save()
                box = box.xyxy[0]
                LinkPhotoPerson.objects.create(BoundingBox=f"{box[0]},{box[1]},{box[2]},{box[3]}", Person=person, Photo=photo).save()
                # Crop the image using the bounding box coordinates and save the cropped image
                image = Image.open(img)
                cropped_image = image.crop((int(box[0]), int(box[1]), int(box[2]), int(box[3])))
                cropped_image_path = f"animalsCropped/{img.split('/')[-1]}"
                cropped_image.save(cropped_image_path)

                cropped_face = CroppedFace.objects.create(Path=cropped_image_path, Person=person, OriginalPhoto=photo)
                cropped_face.save()

    os.rename(img, f"photos/{img.split('/')[-1]}")
    return ((),f"No human, {' '.join(str(i) for i in classes)} in image")




def detectPerson(img, user):
    faces = DeepFace.extract_faces(img, detector_backend='mtcnn')
    image = Image.open(img)
    size = image.size
    padding_sacle = 0.05
    padding = (padding_sacle*size[0], padding_sacle*size[1])
    find_result = {}
    for face in faces:
        face = face['facial_area']
        x1,x2 = max(face['x']-padding[0],0), min(face['x']+face['w']+padding[0], size[0])
        y1,y2 = max(face['y']-padding[1],0), min(face['y']+face['h']+padding[1], size[1])
        cropped_face = image.crop((x1, y1, x2, y2))
        cropped_face.save("temp/cropped_face.png")
        if len(os.listdir("faceDataBase")) == 0:
            face_result = None
        else:
            face_result = DeepFace.find("temp/cropped_face.png", "faceDataBase", enforce_detection=False)
        max_cosine = float('inf')
        max_index = -1
        if face_result is not None:
            for i, df in enumerate(face_result):
                cosine = df['VGG-Face_cosine'].min()
                if cosine < max_cosine:
                    max_cosine = cosine
                    max_index = i

            max_df = face_result[max_index]
            if not max_df.empty:
                max_row = max_df.loc[max_df['VGG-Face_cosine'].idxmin()]
            else:
                max_row = None
        else:
            max_row = None

        if max_row is not None and max_row['VGG-Face_cosine'] <= 0.2:

            identity = max_row['identity'].replace("\\", "/")
            identity = identity.split("/")[-2]
            find_result[len(find_result)]=(face,identity)
            os.remove("temp/cropped_face.png")
            photo = Photo.objects.create(Path=f"photos/{img.split('/')[-1]}", User=user) if not Photo.objects.filter(Path=f"photos/{img.split('/')[-1]}").exists() else Photo.objects.get(Path=f"photos/{img.split('/')[-1]}")
            photo.save() 
            if os.path.exists(img):
                os.rename(img, f"photos/{img.split('/')[-1]}")

            LinkPhotoPerson.objects.create(BoundingBox=f"{x1},{y1},{x2},{y2}", Person=Person.objects.get(pk=identity), Photo=photo).save()

        else:
            person = Person.objects.create(Name='Unknown', User=user)
            person.save()
            person.Name = f"Unknown-{person.id}"
            person.save()
            id = person.id
            os.mkdir(f"faceDataBase/{person.id}")
            os.rename("temp/cropped_face.png", f"faceDataBase/{person.id}/0.png")
            if os.path.exists(img):
                os.rename(img, f"photos/{img.split('/')[-1]}")

            photoObject = Photo.objects.create(Path=f"photos/{img.split('/')[-1]}", User=user, ) if not Photo.objects.filter(Path=f"photos/{img.split('/')[-1]}").exists() else Photo.objects.get(Path=f"photos/{img.split('/')[-1]}")
            photoObject.save()
            link = LinkPhotoPerson.objects.create(BoundingBox=f"{x1},{y1},{x2},{y2}", Person=person, Photo=photoObject)
            link.save()
            croppedFaceObject = CroppedFace.objects.create(Path=f"faceDataBase/{person.id}/0.png", Person=person, OriginalPhoto=photoObject)
            croppedFaceObject.save()

            os.remove("faceDataBase/representations_vgg_face.pkl") if os.path.exists("faceDataBase/representations_vgg_face.pkl") else None

            face_result = (face,"Unknown")
            find_result[id]=face_result

    return find_result

