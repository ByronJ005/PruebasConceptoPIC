# FastAPI Authentication Backend API

This is the backend API for the transport cooperative ticket booking authentication module.

## Stack
- Python 3.10+
- FastAPI
- SQLAlchemy (Sync engine)
- PostgreSQL
- Alembic (Database migrations)

## API Endpoints

- `POST /api/auth/register`: Create user account.
- `POST /api/auth/login`: Authenticate and receive access token (in response body) and refresh token (HttpOnly cookie).
- `POST /api/auth/logout`: Clears the refresh token cookie.
- `POST /api/auth/password-recovery`: Request password recovery link.
- `POST /api/auth/password-reset`: Reset password using the recovery token.
