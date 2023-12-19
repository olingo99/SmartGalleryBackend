from rest_framework import serializers
from .models import Photo, Person, LinkPhotoPerson, CroppedFace


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ["id", "Path", "Date", "Location", "User"]


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ["id", "Name", "User"]


class LinkPhotoPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkPhotoPerson
        fields = ["id", "BoundingBox", "Person", "Photo"]

class CroppedFaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CroppedFace
        fields = ["id","Path", "Person", "OriginalPhoto"]