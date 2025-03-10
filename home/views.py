from rest_framework import viewsets, status
from rest_framework.decorators import api_view, APIView, action
from rest_framework.response import Response
from .serializers import PeopleSerializer , loginSerializer , ColorSerializer ,RegisterSerializer
from .models import Person , Color
from rest_framework import viewsets
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from django.core.exceptions import EmptyResultSet
from rest_framework.exceptions import NotFound
from django.core.paginator import EmptyPage
#login api

class loginAPI(APIView):
     def post(self, request):
         serializer = loginSerializer(data=request.data)
         if not serializer.is_valid():
            
            return Response({
                'status':False,
                'message':serializer.errors
            } ,status=status.HTTP_400_BAD_REQUEST)
            
         user = authenticate(username = serializer.data['username'], password = serializer.data['password'])
         print(user,'user')

         if not user:
                return Response({
                    'status':False,
                    'message':'Invalid credentials'
                }, status=status.HTTP_401_UNAUTHORIZED)
            
         token, _ = Token.objects.get_or_create(user=user)
         return Response({
            'status':True,
            'token': token.key,
            'message': 'User logged in successfully'
            }, status=status.HTTP_200_OK)
       
class PersonPagination(PageNumberPagination):
    page_size = 5  # Default page size
    page_size_query_param = 'per_page'  # Allow dynamic page size
    max_page_size = 100  # Prevent excessive data requests

#register 
class RegisterAPI(APIView):
     def post(self, request):
         serializer = RegisterSerializer(data=request.data)
         if serializer.is_valid():
             user = serializer.save()
             return Response({
                    'user': user,
                    'message': 'User created successfully'
                }, status=status.HTTP_201_CREATED)
             
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Create your views here.
class PersonAPI(APIView):
    def get(self, request):

        return Response("this is get method")

    def post(self, request):
        return Response("this is post method")

    def patch(self, request):
        return Response(" this is patch method")

    def put(self, request):
        return Response("this is put method")
    def delete(self, request):
        return Response("this is delete method")


# login apu api_view 
@api_view(['GET', 'DELETE', 'POST', 'PUT','PATCH'])
def login(request):
    # GET method 
    if request.method == 'POST':
        data = request.data
        serializer = loginSerializer(data=data)
        if(serializer.is_valid()):
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

# color crud operation 
class PeopleViewSet(viewsets.ModelViewSet):
    serializer_class = PeopleSerializer
    queryset = Person.objects.all()
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]  
    pagination_class = PersonPagination  # Use DRF standard pagination

    # ✅ Create a new person
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ✅ Retrieve a single person by ID
    def retrieve(self, request, pk=None):
        try:
            person = self.get_queryset().get(pk=pk)
            serializer = self.get_serializer(person)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Person.DoesNotExist:
            return Response({'error': 'Person not found'}, status=status.HTTP_404_NOT_FOUND)

    # ✅ Update an entire person object (PUT)
    def update(self, request, pk=None):
        try:
            person = self.get_queryset().get(pk=pk)
            serializer = self.get_serializer(person, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Person.DoesNotExist:
            return Response({'error': 'Person not found'}, status=status.HTTP_404_NOT_FOUND)

    # ✅ Partially update a person object (PATCH)
    def partial_update(self, request, pk=None):
        try:
            person = self.get_queryset().get(pk=pk)
            serializer = self.get_serializer(person, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Person.DoesNotExist:
            return Response({'error': 'Person not found'}, status=status.HTTP_404_NOT_FOUND)

    # ✅ Delete a person (DELETE)
    def destroy(self, request, pk=None):
        try:
            person = self.get_queryset().get(pk=pk)
            person.delete()
            return Response({'message': 'Person deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Person.DoesNotExist:
            return Response({'error': 'Person not found'}, status=status.HTTP_404_NOT_FOUND)

    # ✅ List all persons (GET)


    def list(self, request):
        queryset = Person.objects.all()
        paginator = self.pagination_class()

        try:
            paginated_queryset = paginator.paginate_queryset(queryset, request)

            # ✅ If page is out of range, return an empty array instead of an error
            if paginated_queryset is None:
                return Response({
                    "count": queryset.count(),
                    "total_pages": paginator.page.paginator.num_pages if queryset.exists() else 0,
                    "current_page": int(request.query_params.get('page', 1)),
                    "per_page": int(request.query_params.get('per_page', paginator.page_size)),
                    "results": []  # Empty array instead of error
                }, status=status.HTTP_200_OK)

            serializer = PeopleSerializer(paginated_queryset, many=True)
            return paginator.get_paginated_response(serializer.data)

        except EmptyPage:  # Handle out-of-range pages safely
            return Response({
                "count": queryset.count(),
                "total_pages": paginator.page.paginator.num_pages if queryset.exists() else 0,
                "current_page": int(request.query_params.get('page', 1)),
                "per_page": int(request.query_params.get('per_page', paginator.page_size)),
                "results": []
            }, status=status.HTTP_200_OK)

        except Exception as e:  # Catch unexpected errors
            return Response({
                "error": "Something went wrong.",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    @action(detail=False, methods=['post'])
    def send_mail_to_person(self, request, pk=None):
        try:
            return Response({
                'status':True,
                'message':'send email successfully'
            } ,status=status.HTTP_200_OK)
        except Person.DoesNotExist:
            return Response({'error': 'Person not found'}, status=status.HTTP_404_NOT_FOUND)
        except Color.DoesNotExist:
            return Response({'error': 'Color not found'}, status=status.HTTP_404_NOT_FOUND) 

            

      
class ColorViewSet(viewsets.ModelViewSet):
    serializer_class = ColorSerializer
    queryset = Color.objects.all()

    