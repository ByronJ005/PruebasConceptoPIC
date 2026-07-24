# Phase 1: Data Model

This document outlines the core data entities, relationships, and validation rules for the Authentication Module.

## Entities

### User
Represents a customer of the transport cooperative.

**Fields:**
- `id`: UUID (Primary Key)
- `email`: String (Unique, Indexed, Required)
- `password_hash`: String (Required)
- `is_active`: Boolean (Default: true)
- `created_at`: DateTime (Default: now)
- `updated_at`: DateTime (Default: now)

**Relationships:**
- Has Many `PasswordResetToken`

**Validation Rules:**
- `email`: Must be a valid email format (via Pydantic `EmailStr`). Max length 255 chars.
- `password` (pre-hash): Must be at least 8 characters long, contain at least one number and one special character (validated during registration/reset).

**State Transitions:**
- Currently simplistic: Active by default. Future scope might include `is_verified` (Boolean).

---

### PasswordResetToken
Represents a temporary, secure token for password recovery.

**Fields:**
- `id`: UUID (Primary Key)
- `user_id`: UUID (Foreign Key to `User.id`, Indexed, Required)
- `token_hash`: String (Unique, Indexed, Required) - *SHA-256 hash of the securely generated URL-safe token*
- `expires_at`: DateTime (Required)
- `is_used`: Boolean (Default: false)
- `created_at`: DateTime (Default: now)

**Relationships:**
- Belongs to `User`

**Validation Rules:**
- `token` (pre-hash input): Must be URL-safe string.
- Cannot be used if `expires_at` is in the past.
- Cannot be used if `is_used` is true.

**State Transitions:**
- Valid -> Used (when user successfully resets password)
- Valid -> Expired (time-based)
