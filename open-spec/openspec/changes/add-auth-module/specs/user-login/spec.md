## ADDED Requirements

### Requirement: User login with email and password
The system SHALL allow a registered user to authenticate by providing their email and password. On success the system SHALL return a signed JWT access token (HS256, expires in 15 minutes) in the response body and set an `HttpOnly; Secure; SameSite=Lax` cookie named `refresh_token` containing an opaque UUID (expires in 7 days). The access token payload SHALL include `sub` (user id), `email`, `role`, and `exp`.

#### Scenario: Successful login
- **WHEN** a user sends `POST /api/v1/auth/login` with correct email and password
- **THEN** the system returns `200 OK` with `{ "access_token": "...", "token_type": "bearer", "user": { id, email, full_name, role } }` and sets the `refresh_token` cookie

#### Scenario: Wrong password
- **WHEN** a user sends a valid email with an incorrect password
- **THEN** the system returns `401 Unauthorized` with detail `"Invalid credentials"` and does NOT reveal whether the email exists

#### Scenario: Unknown email
- **WHEN** a user sends an email that is not registered
- **THEN** the system returns `401 Unauthorized` with detail `"Invalid credentials"` (same message as wrong password to prevent email enumeration)

#### Scenario: Disabled account
- **WHEN** a user whose account has been deactivated attempts to log in
- **THEN** the system returns `403 Forbidden` with detail `"Account is disabled"`

#### Scenario: Rate limiting on login
- **WHEN** the same IP address sends more than 5 login requests within 60 seconds
- **THEN** the system returns `429 Too Many Requests` with a `Retry-After` header
