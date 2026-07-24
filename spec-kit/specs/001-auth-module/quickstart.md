# Phase 1: Quickstart Validation Guide

This document provides runnable validation scenarios to prove that the Authentication Module works end-to-end.

## Prerequisites

- PostgreSQL database running and accessible.
- Backend server running on `http://localhost:8000`.
- Frontend server running on `http://localhost:5173`.
- `curl` or Postman installed for API testing.

## Setup Commands

1. **Database Migration**:
   ```bash
   cd backend
   alembic upgrade head
   ```
2. **Start Backend**:
   ```bash
   cd backend
   uvicorn src.main:app --reload
   ```
3. **Start Frontend**:
   ```bash
   cd frontend
   npm run dev
   ```

## Validation Scenarios

### Scenario 1: User Registration
**Goal**: Verify a new user can register.
**Command (cURL)**:
```bash
curl -X POST http://localhost:8000/api/auth/register \
     -H "Content-Type: application/json" \
     -d '{"email": "test@example.com", "password": "SecurePassword123!"}'
```
**Expected Outcome**: 
HTTP `201 Created` with a JSON body indicating success. Verify via database tool that the user is present and the password is hashed.

### Scenario 2: User Login
**Goal**: Verify the user can log in and receive a JWT access token and a refresh token cookie.
**Command (cURL)**:
```bash
curl -X POST http://localhost:8000/api/auth/login -i \
     -H "Content-Type: application/json" \
     -d '{"email": "test@example.com", "password": "SecurePassword123!"}'
```
**Expected Outcome**: 
HTTP `200 OK`. The response body must contain an `access_token` and the headers must include a `Set-Cookie` directive for the `refresh_token` (HttpOnly).

### Scenario 3: End-to-End Frontend Flow
**Goal**: Verify the full Vue 3 UI experience.
**Steps**:
1. Open browser at `http://localhost:5173/register`.
2. Enter email and password. Click Register.
3. Observe redirect to login page or automatic login.
4. If not auto-logged in, open `http://localhost:5173/login`.
5. Enter credentials.
6. Verify successful redirect to the application dashboard and presence of user state in Pinia DevTools.
7. Click "Logout" and verify redirection to the login page and clearance of local state.

## Reference
- See [API Contracts](contracts/api-endpoints.md) for full endpoint definitions.
- See [Data Model](data-model.md) for database structure.
