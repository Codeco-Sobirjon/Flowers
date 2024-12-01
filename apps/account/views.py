from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from django.utils.translation import gettext as _
from rest_framework.permissions import IsAuthenticated
from apps.account.models import (
    CustomUser
)
from apps.account.serializers import (
    GroupListSerializer, CustomAuthTokenSerializer,
    SignUpSerializer, CustomUserDeatilSerializer, UpdateUserSerializer, PasswordUpdateSerializer,
)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class UserSignupView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=SignUpSerializer, tags=['Account'])
    def post(self, request, *args, **kwargs):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomAuthTokenView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=CustomAuthTokenSerializer, tags=['Account'])
    def post(self, request):
        serializer = CustomAuthTokenSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoleListView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(responses={200: "List of all available roles"}, tags=['Account'])
    def get(self, request, *args, **kwargs):
        roles = Group.objects.all()
        serializer = GroupListSerializer(roles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomUserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: CustomUserDeatilSerializer()},
        operation_description="Retrieve details of the authenticated user.", tags=['Account']
    )
    def get(self, request):
        user = request.user
        serializer = CustomUserDeatilSerializer(user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=UpdateUserSerializer,
        responses={200: CustomUserDeatilSerializer()},
        operation_description="Update the authenticated user's profile.", tags=['Account']
    )
    def put(self, request):
        user = request.user
        serializer = UpdateUserSerializer(user, data=request.data, partial=True, context={'request': request} )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={204: 'No Content'},
        operation_description="Delete the authenticated user's account.", tags=['Account']
    )
    def delete(self, request):
        user = request.user
        user.delete()
        return Response({"detail": _("User deleted successfully.")}, status=status.HTTP_204_NO_CONTENT)


class PasswordUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=PasswordUpdateSerializer,
        tags=['Account'],
        responses={
            200: "Password updated successfully.",
            400: "Bad Request: Password update failed."
        },
        operation_description="Update the authenticated user's password."
    )
    def patch(self, request):
        serializer = PasswordUpdateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.update(request.user, serializer.validated_data)
            return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
