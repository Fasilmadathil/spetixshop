from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from one.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RegisterSerializer
from rest_framework import generics


# @api_view(['GET', 'POST', 'PUT'])
# def index(request):
#     if request.method == 'GET':
#         people_details = {
#             'name': 'fasil',
#             'age': '23'
#         }
#         return Response(people_details)

#     elif request.method == 'POST':
#         # print('post')

#         return Response('post')

#     elif request.method == 'PUT':
#         # print('PUT')
# return Response('PUT')


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(SignupSerializer, self).create(validated_data)


class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        print(username, password)

        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class ManageUser(APIView):
    # permission_classes = [IsAuthenticated]  # Only allow superusers
    permission_classes = [AllowAny]

    def post(self, request):
        # Add a new user
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if not username or not password or not email:
            return Response({"error": "Username, password, and email are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Create the user
        user = User.objects.create_user(
            username=username, password=password, email=email)
        return Response({"message": "User created successfully.", "user_id": user.id}, status=status.HTTP_201_CREATED)

    def put(self, request, user_id):
        # Edit an existing user
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        username = request.data.get('username', user.username)
        email = request.data.get('email', user.email)

        user.username = username
        user.email = email
        user.save()

        return Response({"message": "User updated successfully."}, status=status.HTTP_200_OK)

    def delete(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return Response({"message": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
