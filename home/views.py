from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PeopleSerializer
from .models import Person
# Create your views here.

@api_view(['GET', 'DELETE', 'POST', 'PUT','PATCH'])
def person(request):
    # GET method 
    if request.method == 'GET':
        obj = Person.objects.all()
        serializer = PeopleSerializer(obj, many=True)
        return Response(serializer.data)
   
   # POST method 
    elif request.method == 'POST':
        data = request.data
        serializer = PeopleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    # PATCH method (Partial Update)
    elif request.method == 'PATCH':
        person_instance = get_object_or_404(Person, id=request.data.get('id'))
        serializer = PeopleSerializer(person_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    # PUT method (Full Update)
    elif request.method == 'PUT':
        person_instance = get_object_or_404(Person, id=request.data.get('id'))
        serializer = PeopleSerializer(person_instance, data=request.data)  # No partial=True
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    # DELETE method
    elif request.method == 'DELETE':
        person_instance = get_object_or_404(Person, id=request.data.get('id'))
        person_instance.delete()
        return Response({"message": "Deleted successfully"}, status=204)

    
