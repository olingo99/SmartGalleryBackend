from django.contrib.auth.models import User
from rest_framework import serializers, views, permissions, status
from rest_framework.response import Response

# Serializer for the User model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

# View for user creation
class CreateUserView(views.APIView):
    permission_classes = [permissions.AllowAny]  # Allow any user (authenticated or not) to access this view

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)