from home.views import  login , PersonAPI, PeopleViewSet , ColorViewSet
from rest_framework.routers import DefaultRouter
from django.contrib import admin
from django.urls import path , include
router = DefaultRouter()
router.register(r'person', PeopleViewSet, basename='person')
router.register(r'color', ColorViewSet, basename='color')
urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
    path('login/', login),  # Ensure the trailing slash is here
    path('api-method-testing/', PersonAPI.as_view(), name='person-api')  # ✅ Correct

]