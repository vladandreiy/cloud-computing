from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from .models import *
from .serializers import*
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.views.decorators.csrf import csrf_exempt


class GetMethod(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def list(self, request, *args, **kwargs):
        data = list(CustomUser.objects.all().values())
        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        data = list(CustomUser.objects.filter(id=kwargs['pk']).values())
        return Response(data)

    def create(self, request, *args, **kwargs):
        user_serializer_data = CustomUserSerializer(data=request.data)

        if user_serializer_data.is_valid():
            user_serializer_data.save()
            status_code = status.HTTP_201_CREATED
            return Response({"message": "User Added Sucessfully", "status": status_code})
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            return Response({"message": "Please fill the datails", "status": status_code})

    def destroy(self, request, *args, **kwargs):
        product_data = CustomUser.objects.filter(id=kwargs['pk'])
        if product_data:
            product_data.delete()
            status_code = status.HTTP_201_CREATED
            return Response({"message": "User deleted Sucessfully", "status": status_code})
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            return Response({"message": "Product data not found", "status": status_code})

    def update(self, request, *args, **kwargs):
        user_details = CustomUser.objects.get(id=kwargs['pk'])
        user_serializer_data = CustomUserSerializer(
            user_details, data=request.data, partial=True)
        if user_serializer_data.is_valid():
            user_serializer_data.save()
            status_code = status.HTTP_201_CREATED
            return Response({"message": "User updated Sucessfully", "status": status_code})
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            return Response({"message": "User data Not found", "status": status_code})

class LoginView(APIView):
    @swagger_auto_schema(
        operation_description="API for user login",
        request_body=openapi.Schema(
       type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='email'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='password'),
            },
        ),
        responses={200: openapi.Response(description='OK')},
    )
    @csrf_exempt 
    def post(self, request, format=None):
        print(request.data)
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class VerifyView(APIView):
    @swagger_auto_schema(manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER, description="Authorization token", type=openapi.TYPE_STRING)])
    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        if token is None:
            return Response({'error': 'No token provided'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            token_obj = Token.objects.get(key=token)
        except Token.DoesNotExist:
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

        if not token_obj.user.is_active:
            return Response({'error': 'User not active'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'message': 'Token is valid'})