## ADDED Requirements

### Requirement: Silent access token renewal
The system SHALL allow an authenticated client to obtain a new access token by presenting a valid refresh token cookie. The endpoint SHALL implement refresh token rotation: it SHALL invalidate the presented token and issue a new one. If a token that has already been used is presented, the system SHALL revoke ALL refresh tokens for that user (detect token theft) and return an error.

#### Scenario: Successful token refresh
- **WHEN** a client sends `POST /api/v1/auth/refresh` with a valid `refresh_token` cookie
- **THEN** the system returns `200 OK` with a new `{ "access_token": "...", "token_type": "bearer" }`, invalidates the old refresh token, and sets a new `refresh_token` cookie with a renewed expiry

#### Scenario: Expired refresh token
- **WHEN** a client presents a refresh token whose expiry date has passed
- **THEN** the system returns `401 Unauthorized` with detail `"Refresh token expired"` and clears the cookie

#### Scenario: Unknown refresh token
- **WHEN** a client presents a refresh token that does not exist in the database
- **THEN** the system returns `401 Unauthorized` with detail `"Invalid refresh token"`

#### Scenario: Reused refresh token (theft detection)
- **WHEN** a client presents a refresh token that was already used in a previous rotation cycle
- **THEN** the system revokes all active refresh tokens for the associated user, returns `401 Unauthorized` with detail `"Refresh token reuse detected — all sessions revoked"`, and clears the cookie

#### Scenario: Missing cookie
- **WHEN** a client sends `POST /api/v1/auth/refresh` without the `refresh_token` cookie
- **THEN** the system returns `401 Unauthorized` with detail `"Refresh token missing"`
