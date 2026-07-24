## Why

El sistema de reserva de boletos del Terminal de Loja requiere un mecanismo seguro para identificar a los usuarios antes de permitirles realizar reservas. Sin autenticación, no es posible asociar reservas a pasajeros concretos, controlar el acceso por rol (pasajero, operador, administrador) ni proteger datos personales y de pago. El módulo de autenticación es el prerequisito técnico y funcional de todas las demás características del sistema.

## What Changes

- Se introduce el registro de nuevos usuarios mediante correo electrónico y contraseña.
- Se habilita el inicio de sesión con emisión de JWT de acceso (15 min) y refresh token rotativo (7 días).
- Se implementa el cierre de sesión con invalidación del refresh token en servidor.
- Se agrega el flujo de recuperación de contraseña mediante correo electrónico con token de un solo uso y expiración corta (1 hora).
- Se establece el sistema de roles (`passenger`, `operator`, `admin`) con middleware de autorización RBAC.
- Se exponen los endpoints bajo `/api/v1/auth/` en el backend FastAPI.
- Se crean las páginas y el store de autenticación en el frontend Vue 3 + Pinia.

## Capabilities

### New Capabilities

- `user-registration`: Registro de nuevos usuarios con validación de correo único, hash de contraseña y asignación de rol por defecto (`passenger`).
- `user-login`: Inicio de sesión con correo y contraseña; emisión de access token JWT y refresh token; devolución del perfil básico del usuario autenticado.
- `token-refresh`: Renovación silenciosa del access token usando el refresh token; rotación del refresh token en cada uso.
- `user-logout`: Cierre de sesión con revocación del refresh token activo en base de datos.
- `password-recovery`: Flujo de dos pasos: solicitud de restablecimiento (envío de email con enlace) y confirmación (token + nueva contraseña).

### Modified Capabilities

*(No hay specs existentes; no aplica.)*

## Impact

- **Backend**: Nuevos modelos ORM (`User`, `RefreshToken`, `PasswordResetToken`), schemas Pydantic, servicios y routers en `app/api/v1/routers/auth.py`. Dependencia nueva: `python-jose`, `passlib[bcrypt]`, `fastapi-mail`.
- **Frontend**: Nuevas páginas (`/register`, `/login`, `/logout`, `/forgot-password`, `/reset-password`), store `useAuthStore` en Pinia, composable `useAuth`, interceptor Axios para inyección del token y renovación silenciosa.
- **Base de datos**: Tres tablas nuevas gestionadas con migraciones Alembic.
- **Infraestructura**: Configuración de servidor SMTP (variable de entorno) para envío de correos. Sin cambios en Docker Compose fuera de las nuevas variables de entorno.
- **Seguridad**: Aplicación de rate limiting en `/auth/login` y `/auth/register`; cookies `HttpOnly` para el refresh token.
