# TerminalLoja – Sistema de Reserva de Boletos en Línea

## Descripción del Proyecto

**TerminalLoja** es una plataforma web que permite a los pasajeros consultar, reservar y gestionar boletos de transporte interprovincial en las cooperativas del Terminal Terrestre de la ciudad de **Loja, Ecuador**.

El sistema centraliza la oferta de rutas de las distintas cooperativas, expone disponibilidad en tiempo real y garantiza un proceso de reserva seguro y trazable para usuarios finales, operadores de cooperativa y administradores del terminal.

---

## Objetivo General

Desarrollar una aplicación web de reserva de boletos que integre múltiples cooperativas de transporte del Terminal de Loja, brindando una experiencia unificada, segura y accesible tanto para pasajeros como para el personal operativo.

---

## Alcance

### Incluido

- Registro y autenticación de usuarios (pasajeros, operadores, administradores).
- Gestión de cooperativas, rutas, horarios y precios.
- Motor de búsqueda y disponibilidad de asientos en tiempo real.
- Reserva, confirmación y cancelación de boletos.
- Panel de administración para cooperativas y operadores.
- Generación de comprobante de reserva (PDF / código QR).
- Historial de viajes del usuario.

### Excluido (MVP)

- Pasarela de pago en línea (se integrará en una fase posterior).
- Aplicación móvil nativa.
- Rastreo GPS de buses en tiempo real.

---

## Stack Tecnológico

### Frontend

| Tecnología | Versión mínima | Propósito |
|---|---|---|
| **Vue 3** | 3.4+ | Framework UI (Composition API) |
| **TypeScript** | 5.x | Tipado estático en todo el frontend |
| **Pinia** | 2.x | Gestión de estado global |
| **Vue Router** | 4.x | Enrutamiento SPA |
| **Vite** | 5.x | Bundler y servidor de desarrollo |
| **Axios** | 1.x | Cliente HTTP |
| **Zod** | 3.x | Validación de esquemas en cliente |

### Backend

| Tecnología | Versión mínima | Propósito |
|---|---|---|
| **Python** | 3.12+ | Lenguaje principal del backend |
| **FastAPI** | 0.111+ | Framework API REST asíncrono |
| **SQLAlchemy** | 2.x | ORM con soporte async |
| **Alembic** | 1.x | Migraciones de base de datos |
| **PostgreSQL** | 15+ | Base de datos relacional |
| **Pydantic v2** | 2.x | Validación y serialización de datos |
| **Passlib + bcrypt** | — | Hash de contraseñas |
| **python-jose** | — | Generación y verificación de JWT |
| **pytest + httpx** | — | Pruebas unitarias e integración |

### Infraestructura y DevOps

| Tecnología | Propósito |
|---|---|
| **Docker / Docker Compose** | Contenedores para dev y producción |
| **GitHub Actions** | CI/CD (lint, tests, build) |
| **Nginx** | Proxy inverso en producción |
| **pgAdmin / DBeaver** | Administración de base de datos |

---

## Arquitectura General

```
┌─────────────────────────────┐
│         Navegador           │
│  Vue 3 + Pinia + TS (SPA)  │
└────────────┬────────────────┘
             │ HTTPS / REST JSON
             ▼
┌─────────────────────────────┐
│   FastAPI  (API REST)       │
│   Autenticación JWT         │
│   Validación Pydantic v2    │
└────────────┬────────────────┘
             │ SQLAlchemy async
             ▼
┌─────────────────────────────┐
│        PostgreSQL           │
│     (Base de datos)         │
└─────────────────────────────┘
```

---

## Convenciones de Desarrollo

### General

- Idioma del código: **inglés** (variables, funciones, clases, comentarios en código).
- Idioma de la documentación: **español** (README, docstrings públicos, wikis).
- Todos los cambios deben pasar por **pull request** con al menos una revisión aprobada.
- **Conventional Commits** obligatorios:
  - `feat:` nueva funcionalidad
  - `fix:` corrección de bug
  - `docs:` documentación
  - `test:` pruebas
  - `refactor:` refactorización sin cambio funcional
  - `chore:` tareas de mantenimiento (deps, CI)

---

### Frontend (Vue 3 + TypeScript)

#### Estructura de carpetas

```
src/
├── assets/          # Recursos estáticos (imágenes, fuentes)
├── components/      # Componentes reutilizables (PascalCase)
│   └── ui/          # Componentes de diseño base (Button, Input, etc.)
├── composables/     # Composables de Vue (useXxx.ts)
├── layouts/         # Layouts de página
├── pages/           # Vistas enrutadas (kebab-case para archivos)
├── router/          # Definición de rutas
├── services/        # Llamadas a la API (api/xxx.service.ts)
├── stores/          # Tiendas Pinia (useXxxStore.ts)
├── types/           # Interfaces y tipos TypeScript
└── utils/           # Funciones de utilidad puras
```

#### Reglas

- **Componentes**: siempre en `PascalCase` (ej. `ReservationCard.vue`).
- **Composables**: prefijo `use` (ej. `useAuth.ts`).
- **Stores de Pinia**: definir con `defineStore`, exportar como `useXxxStore`.
- Preferir `<script setup lang="ts">` en todos los componentes.
- Props tipadas siempre con `defineProps<{...}>()`.
- Emits tipados siempre con `defineEmits<{...}>()`.
- No usar `any`; si es inevitable, documentar el motivo con un comentario `// TODO:`.
- Validar los datos provenientes de la API con **Zod** antes de pasarlos al store.
- Manejar errores HTTP en el interceptor de Axios centralizado (`src/services/http.ts`).

---

### Backend (FastAPI + SQLAlchemy)

#### Estructura de carpetas

```
app/
├── api/
│   └── v1/
│       ├── routers/     # Routers por dominio (routes.py, reservations.py…)
│       └── deps.py      # Dependencias de FastAPI (get_db, get_current_user…)
├── core/
│   ├── config.py        # Settings via pydantic-settings
│   ├── security.py      # JWT, hashing
│   └── exceptions.py    # Manejadores de excepciones globales
├── db/
│   ├── base.py          # Base declarativa SQLAlchemy
│   ├── session.py       # AsyncSession factory
│   └── migrations/      # Alembic
├── models/              # Modelos ORM (un archivo por entidad)
├── schemas/             # Schemas Pydantic (Request / Response)
├── services/            # Lógica de negocio (un archivo por dominio)
├── repositories/        # Acceso a datos (patrón Repository)
└── tests/               # Pruebas con pytest
    ├── unit/
    └── integration/
```

#### Reglas

- **Separación de capas**: Router → Service → Repository → Model. Nunca saltarse capas.
- Usar **async/await** en todos los endpoints y operaciones de base de datos.
- Definir schemas de entrada (`XxxCreate`, `XxxUpdate`) y de salida (`XxxResponse`) separados.
- Nunca exponer el modelo ORM directamente como respuesta; usar siempre el schema de salida.
- Configuración via variables de entorno con `pydantic-settings` (`.env` no versionado).
- Aplicar migraciones con **Alembic**; nunca alterar tablas manualmente.
- Todos los endpoints deben devolver respuestas con el tipo y status HTTP correctos.

---

## Validaciones de Entrada

### Frontend

- Validar formularios con Zod (esquemas en `src/types/schemas/`).
- Mostrar mensajes de error descriptivos próximos al campo fallido.
- Deshabilitar el botón de envío mientras hay una petición en curso.

### Backend

- Pydantic v2 valida automáticamente el body de cada request.
- Agregar validadores personalizados (`@field_validator`) para reglas de negocio (ej. fecha de salida > ahora).
- Retornar `422 Unprocessable Entity` con detalle de campos fallidos (comportamiento por defecto de FastAPI).
- Sanitizar entradas de texto libre para prevenir inyección de datos.

---

## Manejo de Errores

### Frontend

- Interceptor Axios centralizado captura errores HTTP y despacha notificaciones al store de UI.
- Páginas de error dedicadas: `404 NotFound`, `403 Forbidden`, `500 ServerError`.
- Usar `try/catch` en composables asíncronos; nunca dejar promesas sin manejar.

### Backend

- Definir excepciones de dominio en `app/core/exceptions.py`.
- Handler global de excepciones registrado en `main.py` para:
  - `HTTPException` → respuesta estructurada `{ "detail": "..." }`.
  - `ValidationError` → `422` con lista de errores de campo.
  - Excepciones no controladas → `500` con log detallado (sin exponer stack trace al cliente).
- Logging estructurado con `structlog` o `loguru` en todos los servicios.

---

## Buenas Prácticas de Seguridad

| Área | Práctica |
|---|---|
| **Autenticación** | JWT con expiración corta (15 min) + refresh token rotativo |
| **Contraseñas** | Hash con bcrypt (factor de coste >= 12) |
| **Autorización** | RBAC: roles `passenger`, `operator`, `admin` |
| **CORS** | Permitir solo los orígenes del frontend en producción |
| **Headers HTTP** | Configurar `HSTS`, `X-Content-Type-Options`, `X-Frame-Options` vía Nginx |
| **SQL Injection** | Solo consultas parametrizadas vía SQLAlchemy ORM |
| **Secrets** | Nunca en el código fuente; usar variables de entorno o secret manager |
| **Rate Limiting** | Aplicar en endpoints de autenticación (`/auth/login`, `/auth/register`) |
| **Dependencias** | Revisar vulnerabilidades con `pip-audit` (backend) y `npm audit` (frontend) |

---

## Pruebas

### Frontend

- **Vitest** para pruebas unitarias de composables, utils y stores.
- **Vue Testing Library** para pruebas de componentes.
- Cobertura mínima objetivo: **70 %** en lógica de negocio.

### Backend

- **pytest** + **httpx (AsyncClient)** para pruebas de endpoints.
- **pytest-asyncio** para tests asíncronos.
- Base de datos de prueba: PostgreSQL en Docker (misma imagen que producción).
- Cobertura mínima objetivo: **80 %** en servicios y repositorios.
- Los tests deben ejecutarse en CI antes de cualquier merge a `main`.

---

## Variables de Entorno (referencia)

```dotenv
# Backend (.env)
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/terminalLoja
SECRET_KEY=<clave-secreta-aleatoria>
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
ALLOWED_ORIGINS=http://localhost:5173

# Frontend (.env)
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

---

## Glosario de Dominio

| Término | Definición |
|---|---|
| **Cooperativa** | Empresa de transporte registrada en el terminal |
| **Ruta** | Trayecto definido entre origen y destino |
| **Horario** | Instancia de salida de una ruta en fecha y hora específicas |
| **Asiento** | Plaza numerada disponible en un bus para un horario |
| **Reserva** | Acción de bloquear un asiento para un pasajero |
| **Boleto** | Comprobante generado tras confirmar una reserva |
| **Operador** | Personal de la cooperativa con acceso al panel de gestión |

---

*Última actualización: 2026-07-24*
