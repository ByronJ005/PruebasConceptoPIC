# Phase 0: Research & Architecture Decisions

This document captures the technical decisions made to implement the authentication module, resolving ambiguities and selecting appropriate patterns for the mandated technology stack (Vue 3 / FastAPI).

## Decision 1: JWT Session Management

- **Decision**: Use stateless JWT (JSON Web Tokens) with a short-lived Access Token and an HTTP-Only Refresh Token.
- **Rationale**: 
  - FastAPI is highly optimized for stateless JWT validation.
  - Using an HTTP-Only cookie for the refresh token prevents XSS attacks from stealing long-lived credentials, which aligns with the Constitution's "Security Best Practices".
  - Pinia will store the short-lived access token in memory.
- **Alternatives considered**: 
  - Standard Server-Side Sessions (Redis): Rejected due to added infrastructure complexity and the constraint of "Minimalist Architecture (YAGNI)".
  - Storing Access Token in LocalStorage: Rejected due to XSS vulnerability risks.

## Decision 2: Password Recovery Token Generation

- **Decision**: Generate cryptographically secure URL-safe tokens (using Python's `secrets` module), store their hash (SHA-256) in the database with an expiration timestamp (e.g., 15 minutes).
- **Rationale**: 
  - Storing the hash ensures that even if the database is compromised, the tokens cannot be used to hijack accounts.
  - Fast and simple to implement using SQLAlchemy and Python standard library.
- **Alternatives considered**: 
  - Using JWTs for recovery links: Considered, but JWTs cannot be easily revoked if the user generates multiple requests, whereas database-backed tokens can be invalidated.

## Decision 3: Frontend State Management for Auth

- **Decision**: Create a centralized `authStore` using Pinia that handles all API communication for authentication and maintains the user's logged-in state.
- **Rationale**: 
  - Mandated by Constitution (Pinia).
  - Centralizing the logic makes it easier to write unit tests for the authentication flows.
- **Alternatives considered**: 
  - Handling API calls directly in Vue components: Rejected as it violates separation of concerns and makes unit testing much harder.
