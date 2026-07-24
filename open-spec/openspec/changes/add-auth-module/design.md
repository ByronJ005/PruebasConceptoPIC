## Context

El sistema TerminalLoja necesita autenticar a tres tipos de actores: pasajeros, operadores de cooperativa y administradores del terminal. Actualmente no existe ningún mecanismo de identidad; todos los recursos de la API son accesibles sin credenciales. Este diseño establece las decisiones técnicas para el módulo de autenticación sobre la pila FastAPI + Vue 3 definida en `project.md`.

## Goals / Non-Goals

**Goals:**

- Autenticación stateless con JWT de corta duración y refresh token rotativo almacenado en servidor.
- Control de acceso basado en roles (RBAC) con los roles `passenger`, `operator` y `admin`.
- Flujo de recuperación de contraseña por correo electrónico seguro y con expiración.
- Renovación silenciosa del access token en el frontend sin interrumpir la sesión del usuario.
- Revocación explícita del refresh token al cerrar sesión.

**Non-Goals:**

- Autenticación social (OAuth2 con Google, Facebook, etc.) — fase posterior.
- Autenticación multifactor (MFA / TOTP) — fase posterior.
- Pasarela de pagos o firma de transacciones.
- Gestión de permisos granulares por recurso (por ahora solo roles globales).

## Decisions

### D1 — JWT stateless para access token + refresh token almacenado en BD

**Decisión:** El access token es un JWT firmado (HS256) con expiración de 15 minutos. El refresh token es un UUID opaco almacenado en la tabla `refresh_tokens` con su hash SHA-256; se entrega al cliente como cookie `HttpOnly; Secure; SameSite=Lax`.

**Alternativas consideradas:**
- *JWT para ambos tokens*: descartado porque impide la revocación server-side del refresh token sin una blocklist en Redis.
- *Solo sesión en servidor (session cookie)*: descartado porque contradice la arquitectura stateless elegida para la API y dificulta el escalado horizontal.

**Rationale:** El access token de corta duración minimiza la ventana de exposición ante un leak. El refresh token en BD permite invalidación determinista (logout, contraseña comprometida) sin infraestructura adicional de Redis en MVP.

---

### D2 — Cookie HttpOnly para el refresh token

**Decisión:** El refresh token se envía al cliente dentro de una cookie `HttpOnly; Secure; SameSite=Lax`, nunca en el body de la respuesta.

**Alternativas consideradas:**
- *localStorage*: vulnerable a XSS; descartado.
- *Body de la respuesta JSON*: el frontend debería persistirlo; aumenta la superficie de ataque XSS; descartado.

**Rationale:** Las cookies `HttpOnly` son inaccesibles para JavaScript, lo que elimina el vector XSS más común contra refresh tokens.

---

### D3 — Rotación de refresh token en cada uso

**Decisión:** Cada llamada a `/auth/refresh` invalida el refresh token actual y emite uno nuevo. Si se detecta reutilización de un token ya usado (token comprometido), se revocan todos los tokens de la sesión.

**Rationale:** Implementación del patrón "Refresh Token Rotation" del RFC 6749 para detectar robo de token.

---

### D4 — Hash bcrypt (factor 12) para contraseñas

**Decisión:** Las contraseñas se almacenan con `passlib[bcrypt]` con cost factor 12.

**Alternativas consideradas:**
- *Argon2id*: superior en resistencia a GPU; descartado en MVP por complejidad de configuración; candidato para revisión en fase de hardening.

---

### D5 — Token de recuperación de contraseña como UUID almacenado en BD

**Decisión:** El token de restablecimiento es un UUID v4 almacenado en la tabla `password_reset_tokens` con expiración de 1 hora y campo `used_at`. Se envía al usuario como parámetro de URL en el correo.

**Rationale:** Simple de implementar, auditable y con revocación determinista sin necesidad de firma criptográfica adicional.

---

### D6 — Interceptor Axios con renovación silenciosa

**Decisión:** El cliente Vue intercepta respuestas `401 Unauthorized` en el interceptor de respuesta de Axios, llama a `/auth/refresh`, actualiza el access token en el store de Pinia y reintenta la petición original una vez.

**Rationale:** Proporciona experiencia de sesión continua sin requerir acción del usuario cada 15 minutos.

---

### D7 — Rate limiting en endpoints de autenticación

**Decisión:** Se aplicará `slowapi` (integración nativa con FastAPI) para limitar `/auth/login` y `/auth/register` a **5 peticiones / minuto por IP**.

**Rationale:** Mitiga ataques de fuerza bruta y credential stuffing sin infraestructura adicional en MVP.

## Risks / Trade-offs

| Riesgo | Mitigación |
|---|---|
| Refresh token robado de la cookie | `HttpOnly` + rotación + revocación por reutilización detectada |
| Crecimiento ilimitado de la tabla `refresh_tokens` | Job periódico (o trigger) que elimina tokens expirados |
| Envío de correo fallido (SMTP) en recuperación | Respuesta siempre `200` al usuario para no revelar existencia de email; reintentos con cola ligera (fase posterior) |
| Fuerza bruta en `/auth/login` | Rate limiting con `slowapi`; bloqueo temporal de cuenta tras 10 intentos fallidos (fase posterior) |
| Expiración del access token durante operación larga | El interceptor Axios renueva silenciosamente; operaciones idempotentes son seguras de reintentar |

## Migration Plan

1. Ejecutar `alembic revision --autogenerate -m "add auth tables"` para generar la migración con las tres tablas nuevas.
2. Aplicar la migración en el entorno de staging: `alembic upgrade head`.
3. Configurar variables de entorno SMTP en el servidor.
4. Desplegar backend; validar los endpoints con la colección de Postman/httpx de integración.
5. Desplegar frontend; validar flujos E2E manualmente en staging.
6. **Rollback**: `alembic downgrade -1` elimina las tres tablas sin afectar otras.

## Open Questions

- ¿Se debe bloquear la cuenta automáticamente tras N intentos fallidos en MVP, o diferirlo a fase siguiente?
- ¿Se usará un proveedor SMTP externo (SendGrid, SES) o un servidor SMTP propio del terminal?
- ¿El rol `operator` se asigna manualmente por un `admin` o puede solicitarse mediante un flujo de verificación?
