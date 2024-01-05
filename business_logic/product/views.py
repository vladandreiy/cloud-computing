from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from .models import *
from .serializers import*
import requests
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
import json
from django.views.decorators.csrf import csrf_exempt

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
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        url = "http://127.0.0.1:7000/login/"

        credentials = {
            "email": email,
            "password": password
        }

        headers = {
    'Content-Type': 'application/json',
}
        response = requests.post(url, data=json.dumps(credentials), headers=headers)
        print(response.json())

        if response.status_code == 200:
            data = response.json()
            request.session['token'] = data["token"]
            return Response({f"token: {data['token']}"})
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    

class GetMethod(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        data = list(Product.objects.all().values())
        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        data = list(Product.objects.filter(id=kwargs['pk']).values())
        return Response(data)

    @swagger_auto_schema(manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER, description="Authorization token", type=openapi.TYPE_STRING)])
    def create(self, request, *args, **kwargs):
        product_serializer_data = ProductSerializer(data=request.data)
        token = request.session['token']

        headers = {'Authorization': token}
        response = requests.get(f'http://127.0.0.1:7000/verify/', headers=headers)
        if response.status_code != 200:
            return Response({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
    
        if product_serializer_data.is_valid():
            product_serializer_data.save()
            status_code = status.HTTP_201_CREATED
            return Response({"message": "Product Added Sucessfully", "status": status_code})
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            return Response({"message": "please fill the datails", "status": status_code})

    def destroy(self, request, *args, **kwargs):
        product_data = Product.objects.filter(id=kwargs['pk'])
        if product_data:
            product_data.delete()
            status_code = status.HTTP_201_CREATED
            return Response({"message": "Product delete Sucessfully", "status": status_code})
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            return Response({"message": "Product data not found", "status": status_code})

    def update(self, request, *args, **kwargs):
        product_details = Product.objects.get(id=kwargs['pk'])
        product_serializer_data = ProductSerializer(
            product_details, data=request.data, partial=True)
        if product_serializer_data.is_valid():
            product_serializer_data.save()
            status_code = status.HTTP_201_CREATED
            return Response({"message": "Product Update Sucessfully", "status": status_code})
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            return Response({"message": "Product data Not found", "status": status_code})