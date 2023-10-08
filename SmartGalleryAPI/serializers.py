from rest_framework import serializers
from .models import Photo, Person, LinkPhotoPerson


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ["Path", "Date", "Location", "User"]


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ["Name", "User"]


class LinkPhotoPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkPhotoPerson
        fields = ["BoundingBox", "Person", "Photo"]