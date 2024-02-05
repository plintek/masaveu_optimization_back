# User/User_api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import User
from .serializers import UserSerializer
from django.contrib.auth import login, logout
from django.contrib.auth import authenticate
from rest_framework import authentication
from .authentications import CsrfExemptSessionAuthentication


class UsersListApiView(APIView):
    # add permission to check if user is authenticated

    # 1. List all
    def get(self, request, user_id=None):
        '''
        List all the User items for given requested user
        '''
        serializer = None
        if user_id is None:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
        else:
            users = User.objects.get(id=user_id)
            if not users:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = UserSerializer(users)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # # 2. Create
    # def post(self, request, *args, **kwargs):
    #     '''
    #     Create the User with given User data
    #     '''
    #     data = {
    #         'username': request.data.get('username'),
    #         'email': request.data.get('email'),
    #         'password': request.data.get('password'),

    #     }
    #     serializer = UserSerializer(data=data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)

    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        '''
        Logins and save to cookies
        '''
        user = authenticate(request, username=request.data.get(
            "username"), password=request.data.get("password"))
        if (user is not None):
            login(request, user)
            user = request.user
            serializedData = UserSerializer(user, many=False).data
            response = Response({"isLogged": True, "user": serializedData},
                                status=status.HTTP_200_OK)
        else:
            response = Response(
                {"isLogged": False, "error": "User or password not valid"}, status=status.HTTP_401_UNAUTHORIZED)

        return response


class CheckLogin(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        '''
        Check if user is logged
        '''
        user = request.user

        if (user):

            if (user.is_authenticated):
                serializedData = UserSerializer(user, many=False).data
                del serializedData['password']
                response = Response({"isLogged": True, "user": serializedData},
                                    status=status.HTTP_200_OK)
            else:
                response = Response({"isLogged": False, "error": "User not logged in"},
                                    status=status.HTTP_401_UNAUTHORIZED)
        else:
            response = Response({"isLogged": False, "error": "User not logged in"},
                                status=status.HTTP_401_UNAUTHORIZED)

        return response


class LogOut(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        '''
        Logs out a user
        '''
        logout(request)

        response = Response("Success: User logged out", status=status.HTTP_200_OK)

        return response
