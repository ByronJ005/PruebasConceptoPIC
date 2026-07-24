## ADDED Requirements

### Requirement: User logout with server-side token revocation
The system SHALL allow an authenticated user to log out by revoking their current refresh token on the server side. The endpoint SHALL be accessible with a valid access token OR a valid refresh token cookie (to handle expired access tokens). Upon logout the `refresh_token` cookie SHALL be cleared from the client.

#### Scenario: Successful logout with valid access token
- **WHEN** an authenticated user sends `POST /api/v1/auth/logout` with a valid `Authorization: Bearer <access_token>` header and a `refresh_token` cookie
- **THEN** the system marks the refresh token as revoked in the database, returns `200 OK` with `{ "message": "Logged out successfully" }`, and sets `Set-Cookie: refresh_token=; Max-Age=0` to clear the cookie

#### Scenario: Logout with only refresh token cookie (expired access token)
- **WHEN** a user sends `POST /api/v1/auth/logout` without a valid access token but with a valid `refresh_token` cookie
- **THEN** the system revokes the refresh token, returns `200 OK`, and clears the cookie

#### Scenario: Logout with no credentials
- **WHEN** a client sends `POST /api/v1/auth/logout` without any token
- **THEN** the system returns `401 Unauthorized` with detail `"Authentication required"`

#### Scenario: Already logged out
- **WHEN** a user attempts to log out with a refresh token that was already revoked
- **THEN** the system returns `200 OK` (idempotent) and clears the cookie
