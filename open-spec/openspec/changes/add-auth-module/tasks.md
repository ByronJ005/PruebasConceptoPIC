## 1. Base de datos y modelos ORM

- [x] 1.1 Crear modelo `User` con campos `id`, `email`, `full_name`, `hashed_password`, `role`, `is_active`, `created_at`, `updated_at`
- [x] 1.2 Crear modelo `RefreshToken` con campos `id`, `user_id` (FK), `token_hash` (SHA-256), `expires_at`, `revoked_at`, `created_at`
- [x] 1.3 Crear modelo `PasswordResetToken` con campos `id`, `user_id` (FK), `token_hash`, `expires_at`, `used_at`, `created_at`
- [x] 1.4 Generar migración Alembic `add_auth_tables` y verificarla contra los modelos
- [x] 1.5 Aplicar migración en la base de datos de desarrollo con `alembic upgrade head`

## 2. Seguridad y utilidades del core

- [x] 2.1 Implementar `app/core/security.py`: funciones `hash_password`, `verify_password` con `passlib[bcrypt]` (cost 12)
- [x] 2.2 Implementar `create_access_token(data, expires_delta)` y `decode_access_token(token)` con `python-jose`
- [x] 2.3 Implementar `generate_refresh_token()` → UUID v4 y `hash_token(token)` → SHA-256
- [x] 2.4 Agregar configuración de `SECRET_KEY`, `ACCESS_TOKEN_EXPIRE_MINUTES`, `REFRESH_TOKEN_EXPIRE_DAYS` en `app/core/config.py` usando `pydantic-settings`

## 3. Repositorios

- [x] 3.1 Implementar `UserRepository` con métodos: `get_by_email`, `get_by_id`, `create`, `update_password`
- [x] 3.2 Implementar `RefreshTokenRepository` con métodos: `create`, `get_by_hash`, `revoke`, `revoke_all_for_user`
- [x] 3.3 Implementar `PasswordResetTokenRepository` con métodos: `create`, `get_valid_by_hash`, `invalidate_previous`, `mark_used`

## 4. Schemas Pydantic

- [x] 4.1 Crear `RegisterRequest` (email, password, full_name) con validadores de formato de email y complejidad de contraseña
- [x] 4.2 Crear `LoginRequest` (email, password)
- [x] 4.3 Crear `UserResponse` (id, email, full_name, role) — sin hash de contraseña
- [x] 4.4 Crear `TokenResponse` (access_token, token_type, user: UserResponse)
- [x] 4.5 Crear `ForgotPasswordRequest` (email) y `ResetPasswordRequest` (token, new_password)
- [x] 4.6 Crear `MessageResponse` (message) para respuestas genéricas

## 5. Servicios de autenticación

- [x] 5.1 Implementar `AuthService.register_user(data)` → valida email único, hashea contraseña, crea usuario con rol `passenger`
- [x] 5.2 Implementar `AuthService.login(data, response)` → verifica credenciales, emite access token JWT, genera refresh token y lo persiste; establece cookie `HttpOnly`
- [x] 5.3 Implementar `AuthService.refresh_tokens(request, response)` → lee cookie, verifica token, detecta reutilización, rota tokens
- [x] 5.4 Implementar `AuthService.logout(request, response)` → revoca refresh token de BD, limpia cookie; opera con access token expirado si hay cookie válida
- [x] 5.5 Implementar `AuthService.request_password_reset(email)` → invalida tokens previos, genera nuevo token, envía correo con enlace
- [x] 5.6 Implementar `AuthService.confirm_password_reset(token, new_password)` → valida token, actualiza contraseña, revoca todos los refresh tokens del usuario

## 6. Dependencias FastAPI

- [x] 6.1 Implementar `get_current_user(token)` en `app/api/v1/deps.py` → decodifica JWT y retorna el usuario activo
- [x] 6.2 Implementar `require_role(*roles)` → dependencia de autorización RBAC
- [x] 6.3 Configurar `slowapi` (rate limiter): 5 req/min por IP para `/auth/login` y `/auth/register`

## 7. Router de autenticación

- [x] 7.1 Crear `app/api/v1/routers/auth.py` y registrarlo en `app/main.py` con prefijo `/api/v1/auth`
- [x] 7.2 Implementar `POST /auth/register` → llama `AuthService.register_user`, retorna `201` con `UserResponse`
- [x] 7.3 Implementar `POST /auth/login` → llama `AuthService.login`, retorna `200` con `TokenResponse`
- [x] 7.4 Implementar `POST /auth/refresh` → llama `AuthService.refresh_tokens`, retorna `200` con nuevo `access_token`
- [x] 7.5 Implementar `POST /auth/logout` → llama `AuthService.logout`, retorna `200` con `MessageResponse`
- [x] 7.6 Implementar `POST /auth/forgot-password` → llama `AuthService.request_password_reset`, retorna `200` con `MessageResponse`
- [x] 7.7 Implementar `POST /auth/reset-password` → llama `AuthService.confirm_password_reset`, retorna `200` con `MessageResponse`

## 8. Correo electrónico

- [x] 8.1 Configurar `fastapi-mail` con variables `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`, `EMAILS_FROM_EMAIL` en `config.py`
- [x] 8.2 Crear plantilla HTML de correo para recuperación de contraseña con enlace tokenizado
- [x] 8.3 Implementar `EmailService.send_password_reset(to_email, reset_url)` usando `fastapi-mail` con `BackgroundTasks`

## 9. Frontend — Store y composable

- [x] 9.1 Crear `src/stores/useAuthStore.ts` con estado `user`, `accessToken`, `isAuthenticated` y acciones `login`, `logout`, `refreshToken`
- [x] 9.2 Crear `src/composables/useAuth.ts` que envuelva el store y exponga helpers (`loginUser`, `logoutUser`, `registerUser`)
- [x] 9.3 Configurar interceptor Axios en `src/services/http.ts`: inyectar `Authorization: Bearer` en cada request; capturar `401` y llamar silenciosamente a `POST /auth/refresh` antes de reintentar

## 10. Frontend — Páginas de autenticación

- [x] 10.1 Crear página `src/pages/auth/login.vue` con formulario (email, contraseña), validación Zod, manejo de error `401`
- [x] 10.2 Crear página `src/pages/auth/register.vue` con formulario (nombre, email, contraseña), validación Zod, manejo de error `409`
- [x] 10.3 Crear página `src/pages/auth/forgot-password.vue` con formulario (email) y mensaje de confirmación genérico
- [x] 10.4 Crear página `src/pages/auth/reset-password.vue` con formulario (nueva contraseña, confirmación), lee el token de los query params, maneja errores `400` y `422`
- [x] 10.5 Implementar guard de ruta en `src/router/index.ts` para rutas protegidas: redirigir a `/login` si `!isAuthenticated`

## 11. Pruebas backend

- [x] 11.1 Pruebas unitarias de `AuthService.register_user`: email duplicado, contraseña débil, caso feliz
- [x] 11.2 Pruebas unitarias de `AuthService.login`: credenciales correctas, contraseña errónea, cuenta deshabilitada
- [x] 11.3 Pruebas unitarias de `AuthService.refresh_tokens`: rotación exitosa, token expirado, detección de reutilización
- [x] 11.4 Pruebas unitarias de `AuthService.logout`: revocación exitosa, idempotencia
- [x] 11.5 Pruebas unitarias de `AuthService.request_password_reset` y `confirm_password_reset`: token válido, expirado, ya usado
- [x] 11.6 Pruebas de integración (httpx `AsyncClient`) para todos los endpoints del router `/auth`
- [x] 11.7 Verificar cobertura >= 80% en servicios y repositorios de autenticación

## 12. Pruebas frontend

- [x] 12.1 Pruebas unitarias (Vitest) del `useAuthStore`: estado inicial, mutaciones de login/logout, manejo de errores de red
- [x] 12.2 Pruebas del composable `useAuth`: flujos de registro, login y cierre de sesión con mocks de Axios
- [x] 12.3 Pruebas de componente (Vue Testing Library) para `LoginPage`: renderizado, envío de formulario, mensaje de error

## 13. Calidad y validación final

- [x] 13.1 Ejecutar `pip-audit` en el backend y `npm audit` en el frontend; resolver vulnerabilidades altas
- [x] 13.2 Revisar que ningún endpoint filtre hash de contraseña, stack trace ni información de existencia de email
- [x] 13.3 Probar manualmente el flujo completo: registro → login → refresh silencioso → logout → recuperación de contraseña
- [x] 13.4 Validar cabeceras de seguridad en respuestas: `Set-Cookie` con `HttpOnly; Secure; SameSite=Lax` para el refresh token
- [x] 13.5 Actualizar `README.md` con instrucciones de configuración de variables de entorno de autenticación
