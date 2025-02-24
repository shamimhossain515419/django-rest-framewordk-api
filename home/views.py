from rest_framework import viewsets, status
from rest_framework.decorators import api_view , APIView
from rest_framework.response import Response
from .serializers import PeopleSerializer , loginSerializer , ColorSerializer
from .models import Person , Color
from rest_framework import viewsets
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
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ColorViewSet(viewsets.ModelViewSet):
    serializer_class = ColorSerializer
    queryset = Color.objects.all()

    