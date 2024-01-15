from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import User
from .serializers import UserSerializer, UserDetailedSerializer
from django.contrib.auth import login, logout, authenticate
from .authentications import CsrfExemptSessionAuthentication


class UsersListApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id=None):
        '''
        List all User items for the requested user
        '''
        serializer = None
        if user_id is None:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
        else:
            users = User.objects.get(id=user_id)
            if not users:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = UserDetailedSerializer(users)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserLogin(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        '''
        Log in and save to cookies
        '''
        user = authenticate(request, username=request.data.get(
            "username"), password=request.data.get("password"))
        if user is not None:
            login(request, user)
            user = request.user
            serialized_data = UserSerializer(user, many=False).data
            response = Response(
                {"isLogged": True, "user": serialized_data}, status=status.HTTP_200_OK)
        else:
            response = Response(
                {"isLogged": False, "error": "User or password not valid"}, status=status.HTTP_401_UNAUTHORIZED)

        return response


class CheckLogin(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        '''
        Check if user is logged in
        '''
        user = request.user

        if user:
            if user.is_authenticated:
                serialized_data = UserSerializer(user, many=False).data
                del serialized_data['password']
                response = Response(
                    {"isLogged": True, "user": serialized_data}, status=status.HTTP_200_OK)
            else:
                response = Response(
                    {"isLogged": False, "error": "User not logged in"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            response = Response(
                {"isLogged": False, "error": "User not logged in"}, status=status.HTTP_401_UNAUTHORIZED)

        return response


class LogOut(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        '''
        Log out a user
        '''
        logout(request)

        response = Response("Success: User logged out",
                            status=status.HTTP_200_OK)

        return response


class FollowUser(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        '''
        Follow a user
        '''
        user = request.user
        try:
            user_to_follow = User.objects.get(id=request.data.get("user_id"))
        except:
            return Response({'detail': 'User does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        if user_to_follow in user.following.all():
            return Response({'detail': 'You already follow this user.'}, status=status.HTTP_400_BAD_REQUEST)
        user.following.add(user_to_follow)
        user.following_count += 1
        user_to_follow.followers.add(user)
        user_to_follow.followers_count += 1
        user.save()
        user_to_follow.save()
        serialized_data = UserSerializer(user, many=False).data
        return Response(serialized_data, status=status.HTTP_200_OK)


class UnfollowUser(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        '''
        Unfollow a user
        '''
        user = request.user
        try:
            user_to_unfollow = User.objects.get(id=request.data.get("user_id"))
        except:
            return Response({'detail': 'User does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        if user_to_unfollow not in user.following.all():
            return Response({'detail': 'You do not follow this user.'}, status=status.HTTP_400_BAD_REQUEST)
        user.following.remove(user_to_unfollow)
        user.following_count -= 1
        user_to_unfollow.followers.remove(user)
        user_to_unfollow.followers_count -= 1
        user.save()
        user_to_unfollow.save()
        serialized_data = UserSerializer(user, many=False).data
        return Response(serialized_data, status=status.HTTP_200_OK)


class BlockUser(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        '''
        Block a user
        '''
        user = request.user
        user_to_block_id = request.data.get("user_id")
        try:
            user_to_block = User.objects.get(id=user_to_block_id)
        except User.DoesNotExist:
            return Response({'detail': 'User does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        if user_to_block in user.blocked.all():
            return Response({'detail': 'You already block this user.'}, status=status.HTTP_400_BAD_REQUEST)
        user.blocked_users.add(user_to_block)
        user.save()
        return Response({'message', 'User blocked'}, status=status.HTTP_200_OK)


class UnblockUser(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        '''
        UnBlock a user
        '''
        user = request.user
        user_to_block_id = request.data.get("user_id")
        try:
            user_to_unblock = User.objects.get(id=user_to_block_id)
        except User.DoesNotExist:
            return Response({'detail': 'User does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        if user_to_unblock not in user.blocked.all():
            return Response({'detail': 'You do not block this user.'}, status=status.HTTP_400_BAD_REQUEST)
        user.blocked.remove(user_to_unblock)
        user.save()
        serialized_data = UserSerializer(user, many=False).data
        return Response(serialized_data, status=status.HTTP_200_OK)
