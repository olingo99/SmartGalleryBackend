from rest_framework import serializers
from .models import Photo, Person, LinkPhotoPerson, CroppedFace


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ["id","Path", "Date", "Location", "User", "Tag", "Persons"]


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ["Name", "User"]


class LinkPhotoPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkPhotoPerson
        fields = ["BoundingBox", "Person", "Photo"]

class CroppedFaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CroppedFace
        fields = ["Path", "Person", "OriginalPhoto"]