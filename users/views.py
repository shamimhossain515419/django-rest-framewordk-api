from rest_framework.generics import RetrieveUpdateAPIView  ,CreateAPIView
from rest_framework.permissions import IsAuthenticated , AllowAny ,OR
from .serializers import CustomUserSerializer ,RegisterUserSerializer , LoginUserSerializer ,BlogSerializer
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsAdmin,  IsAdminOrManager ,IsManager

from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import InvalidToken ,TokenError 
from .models import Blog
from django.shortcuts import get_object_or_404
from django.db.models import Q
User = get_user_model()


class UserInfoView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated
    serializer_class = CustomUserSerializer

    def get_queryset(self):
        # Restrict queryset to only the authenticated user
        return User.objects.filter(id=self.request.user.id)

    def get_object(self):
        # Return the authenticated user instance directly
        return self.request.user

class UserRegistrationView(CreateAPIView):
    permission_classes = [AllowAny]  # Override IsAuthenticated
    serializer_class = RegisterUserSerializer


class LoginView(APIView):
    permission_classes = [AllowAny]  # Override IsAuthenticated
    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            
            response = Response({
                "user": CustomUserSerializer(user).data},
                                status=status.HTTP_200_OK)
            
            response.set_cookie(key="access_token", 
                                value=access_token,
                                httponly=True,
                                secure=True,
                                samesite="None")
            
            response.set_cookie(key="refresh_token",
                                value=str(refresh),
                                httponly=True,
                                secure=True,
                                samesite="None")
            return response
        return Response( serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
        
class LogoutView(APIView):
    
    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")
        
        if refresh_token:
            try:
                refresh = RefreshToken(refresh_token)
                refresh.blacklist()
            except Exception as e:
                return Response({"error":"Error invalidating token:" + str(e) }, status=status.HTTP_400_BAD_REQUEST)
        
        response = Response({"message": "Successfully logged out!"}, status=status.HTTP_200_OK)
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        
        return response    



class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request):
        # Retrieve refresh token from cookies
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response({"error": "Refresh token not provided"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            # Decode the refresh token
            refresh = RefreshToken(refresh_token)

            # Get user ID from token payload
            user_id = refresh.payload.get("user_id")  # Use 'user_id' instead of 'user'

            if not user_id:
                return Response({"error": "Invalid refresh token payload"}, status=status.HTTP_401_UNAUTHORIZED)

            # Get the user instance
            user = User.objects.get(id=user_id)

            # Generate new tokens
            new_refresh_token = str(RefreshToken.for_user(user))
            new_access_token = str(AccessToken.for_user(user))

            # Create response
            response = Response(
                {"message": "Access and refresh tokens refreshed successfully"},
                status=status.HTTP_200_OK,
            )

            # Set updated access and refresh tokens in cookies
            response.set_cookie(
                key="access_token",
                value=new_access_token,
                httponly=True,
                secure=True,
                samesite="None",
            )
            response.set_cookie(
                key="refresh_token",
                value=new_refresh_token,
                httponly=True,
                secure=True,
                samesite="None",
            )

            return response

        except (InvalidToken, TokenError, User.DoesNotExist):
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
   

# blog  operations
# List and Create Blogs
class BlogListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrManager]  # Ensure the user is authenticated
    def get(self, request):
        query = request.query_params.get("search",None) # search parameters
        # optimize related data fetching
        blogs = Blog.objects.all()
        # Apply search filters if query is provided
        if query:
            blogs = blogs.filter(
                Q(title__icontains=query) |  # Search by title
                Q(content__icontains=query)|   # Search by content
                Q(author__email__icontains=query)  # Search by author username
            )
        serializer = BlogSerializer(blogs, many=True)
       

        return Response(
          {"data": serializer.data, "status": "success"},
          status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve, Update, and Delete Blog
class BlogDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Blog, pk=pk)

    def get(self, request, pk):
        blog = self.get_object(pk)
        serializer = BlogSerializer(blog)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        blog = self.get_object(pk)
        self.check_object_permissions(request, blog)
        serializer = BlogSerializer(blog, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        blog = self.get_object(pk)
        self.check_object_permissions(request, blog)
        blog.delete()
        return Response({"message": "Blog deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    




