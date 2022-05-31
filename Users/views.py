import uuid
# Create your views here.
from django.contrib.auth import login
from rest_framework import generics, status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from Users.models import User
from Users.serializers import RegisterSerializer

""" User registration view """


class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    """ Post method to handle post 
    request and create a new user """

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "Message": "User created successfully",
                "User": serializer.data}, status=status.HTTP_201_CREATED
            )
        else:
            return Response({"Errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPI(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


class HomeView(APIView):
    permission_classes = (IsAuthenticated,)
    model = User
    template_name = "base.html"

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)
