from django.urls import path , include
from .views import UserInfoView , UserRegistrationView ,LoginView, LogoutView, CookieTokenRefreshView, BlogListCreateAPIView, BlogDetailAPIView
urlpatterns = [
    path('user-info/', UserInfoView.as_view(),name="user-info"),
    path('registration/', UserRegistrationView.as_view(),name="registration"),
    path("login/", LoginView.as_view(), name="user-login"),
    path("logout/", LogoutView.as_view(), name="user-logout"),
    path("refresh/", CookieTokenRefreshView.as_view(), name="token-refresh"),
    path('blogs/', BlogListCreateAPIView.as_view(), name='blog-list-create'),
    path('blogs/<int:pk>/', BlogDetailAPIView.as_view(), name='blog-detail'),
]
