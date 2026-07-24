## ADDED Requirements

### Requirement: Password recovery via email — request step
The system SHALL allow any user to request a password reset by submitting their email address. The system SHALL always respond with `200 OK` regardless of whether the email exists (to prevent email enumeration). If the email is registered, the system SHALL generate a cryptographically random UUID token, store its SHA-256 hash in `password_reset_tokens` with a 1-hour expiry, and send an email to the user containing a reset URL with the plaintext token as a query parameter.

#### Scenario: Request with registered email
- **WHEN** a user sends `POST /api/v1/auth/forgot-password` with a registered email
- **THEN** the system creates a reset token record, sends a recovery email, and returns `200 OK` with `{ "message": "If the email is registered you will receive a password reset link." }`

#### Scenario: Request with unknown email
- **WHEN** a user sends `POST /api/v1/auth/forgot-password` with an email that is not registered
- **THEN** the system returns `200 OK` with the same message as a registered email (no enumeration)

#### Scenario: Multiple reset requests
- **WHEN** a user requests a reset while a valid token already exists
- **THEN** the system invalidates all previous unused tokens for that email and issues a new one

### Requirement: Password recovery via email — confirmation step
The system SHALL allow a user to set a new password by submitting a valid, unexpired, unused reset token together with the new password. Upon success the token SHALL be marked as used and all active refresh tokens for the user SHALL be revoked (force re-login on all devices). The new password SHALL meet the same complexity rules as registration.

#### Scenario: Successful password reset
- **WHEN** a user sends `POST /api/v1/auth/reset-password` with a valid token and a new password that meets complexity rules
- **THEN** the system updates the password hash, marks the token as used, revokes all refresh tokens for the user, and returns `200 OK` with `{ "message": "Password updated successfully." }`

#### Scenario: Expired token
- **WHEN** a user submits a reset token that has passed its 1-hour expiry
- **THEN** the system returns `400 Bad Request` with detail `"Reset token expired or invalid"`

#### Scenario: Already used token
- **WHEN** a user attempts to use a token that has already been consumed
- **THEN** the system returns `400 Bad Request` with detail `"Reset token expired or invalid"` (same message to avoid leaking state)

#### Scenario: Invalid token
- **WHEN** a user submits a token that does not match any record
- **THEN** the system returns `400 Bad Request` with detail `"Reset token expired or invalid"`

#### Scenario: Weak new password
- **WHEN** a user submits a reset token that is valid but the new password fails complexity rules
- **THEN** the system returns `422 Unprocessable Entity` with a field-level error and does NOT consume the token
