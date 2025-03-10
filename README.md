# django-rest-framewordk-api
Djangp rest framework simple Curd operation
# JWT-HTTPCookies-Django-DRF-NEXT.JS
# Django API for User Authentication and Management

This Django project provides API endpoints for user authentication and management. It includes functionality for user registration, login, logout, fetching user information, and token refresh.

## Endpoints

### 1. **User Info**

**URL**: `/user-info/`  
**Method**: `GET`  
**Description**: Fetches the authenticated user's information.  
**Response**:  
- `200 OK`: Returns user data (e.g., username, email).

---

### 2. **User Registration**

**URL**: `/register/`  
**Method**: `POST`  
**Description**: Registers a new user.  
**Request Body**:  
- `username`: The desired username for the new user.
- `email`: The email address of the user.
- `password`: The desired password for the user.

**Response**:  
- `201 Created`: Returns a success message or the created user data.

---

### 3. **User Login**

**URL**: `/login/`  
**Method**: `POST`  
**Description**: Logs in a user and returns authentication tokens.  
**Request Body**:  
- `username`: The username of the user.
- `password`: The password of the user.

**Response**:  
- `200 OK`: Returns an access token and a refresh token if credentials are valid.

---

### 4. **User Logout**

**URL**: `/logout/`  
**Method**: `POST`  
**Description**: Logs out a user and invalidates the session or token.  
**Response**:  
- `200 OK`: Confirms the user is logged out.

---

### 5. **Token Refresh**

**URL**: `/refresh/`  
**Method**: `POST`  
**Description**: Refreshes the access token using the refresh token stored in the user's cookies.  
**Response**:  
- `200 OK`: Returns a new access token.
- `401 Unauthorized`: If the refresh token is invalid or expired.

---

## Requirements

- Python 3.x
- Django 3.x or later
- Django Rest Framework (DRF)

## Installation

1. Clone this repository to your local machine.
2. Navigate to the project folder.
3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
