# Phase 1: API Interface Contracts

This document defines the REST API endpoints exposed by the FastAPI backend to the Vue 3 frontend for the Authentication Module.

## Endpoints

### 1. User Registration
- **URL**: `POST /api/auth/register`
- **Description**: Creates a new user account.
- **Request Body** (JSON):
  ```json
  {
    "email": "user@example.com",
    "password": "SecurePassword123!"
  }
  ```
- **Responses**:
  - `201 Created`: User successfully registered.
    ```json
    {
      "message": "User registered successfully",
      "user_id": "uuid"
    }
    ```
  - `400 Bad Request`: Validation error (e.g., weak password, invalid email).
  - `409 Conflict`: Email already exists.

### 2. User Login
- **URL**: `POST /api/auth/login`
- **Description**: Authenticates a user and issues JWT tokens.
- **Request Body** (JSON or Form Data depending on standard; JSON preferred for modern SPAs):
  ```json
  {
    "email": "user@example.com",
    "password": "SecurePassword123!"
  }
  ```
- **Responses**:
  - `200 OK`: Authentication successful.
    - **Body**: 
      ```json
      {
        "access_token": "jwt.string.here",
        "token_type": "bearer"
      }
      ```
    - **Headers**: `Set-Cookie: refresh_token=...; HttpOnly; Secure; SameSite=Strict`
  - `401 Unauthorized`: Invalid credentials.

### 3. User Logout
- **URL**: `POST /api/auth/logout`
- **Description**: Logs out a user by invalidating the refresh token cookie.
- **Headers**: `Authorization: Bearer <access_token>`
- **Responses**:
  - `200 OK`: Logout successful.
    - **Headers**: `Set-Cookie: refresh_token=; Max-Age=0`

### 4. Password Recovery - Request Reset
- **URL**: `POST /api/auth/password-recovery`
- **Description**: Initiates the password recovery process.
- **Request Body** (JSON):
  ```json
  {
    "email": "user@example.com"
  }
  ```
- **Responses**:
  - `200 OK`: Recovery email sent (or standard generic success message to prevent email enumeration).

### 5. Password Recovery - Reset Password
- **URL**: `POST /api/auth/password-reset`
- **Description**: Resets the password using a valid recovery token.
- **Request Body** (JSON):
  ```json
  {
    "token": "url-safe-token-string",
    "new_password": "NewSecurePassword123!"
  }
  ```
- **Responses**:
  - `200 OK`: Password reset successfully.
  - `400 Bad Request`: Invalid or expired token, or weak password.
