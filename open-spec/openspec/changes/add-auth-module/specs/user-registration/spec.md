## ADDED Requirements

### Requirement: New user registration
The system SHALL allow any unauthenticated visitor to create an account by providing a unique email address, a password that meets complexity rules, and their full name. Upon successful registration the user SHALL receive the role `passenger` by default. The password SHALL be stored as a bcrypt hash (cost factor >= 12); the plaintext password SHALL never be persisted or logged.

#### Scenario: Successful registration
- **WHEN** a visitor sends `POST /api/v1/auth/register` with a valid email, password, and full name
- **THEN** the system creates a new user record with role `passenger`, returns `201 Created` with the user profile (id, email, full_name, role) and does NOT return the password hash

#### Scenario: Duplicate email
- **WHEN** a visitor attempts to register with an email that already exists in the system
- **THEN** the system returns `409 Conflict` with detail `"Email already registered"`

#### Scenario: Weak password
- **WHEN** a visitor submits a password shorter than 8 characters or without at least one uppercase letter, one lowercase letter, and one digit
- **THEN** the system returns `422 Unprocessable Entity` with a field-level error describing the violated rule

#### Scenario: Invalid email format
- **WHEN** a visitor submits a string that is not a valid email address
- **THEN** the system returns `422 Unprocessable Entity` with a field-level error on the `email` field

#### Scenario: Rate limiting
- **WHEN** the same IP address sends more than 5 registration requests within 60 seconds
- **THEN** the system returns `429 Too Many Requests` with a `Retry-After` header
