# TerminalLoja – Sistema de Reserva de Boletos

Módulo de Autenticación y Gestión de Identidad.

## Configuración del Entorno

### Backend

Crea un archivo `.env` en la raíz de la carpeta `backend/` con las siguientes variables:

```dotenv
DATABASE_URL=postgresql+asyncpg://postgres:basepg123@localhost:5432/ticket_booking_os_db
SECRET_KEY=super-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
ALLOWED_ORIGINS=http://localhost:5173

# SMTP (para envío de correo de recuperación de contraseña)
SMTP_HOST=localhost
SMTP_PORT=1025
SMTP_USER=test
SMTP_PASSWORD=password
EMAILS_FROM_EMAIL=noreply@terminalloja.com
```

Para correr las migraciones:
```bash
cd backend
venv\Scripts\python.exe -m alembic.config -c alembic.ini upgrade head
```

Para correr las pruebas del backend:
```bash
cd backend
venv\Scripts\python.exe -m pytest --cov=src tests
```

Para levantar el servidor de desarrollo:
```bash
cd backend
venv\Scripts\python.exe -m uvicorn src.main:app --reload
```

---

### Frontend

Crea un archivo `.env` en la raíz de la carpeta `frontend/` con las siguientes variables:

```dotenv
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

Para instalar dependencias:
```bash
cd frontend
npm install --legacy-peer-deps
```

Para levantar el servidor de desarrollo:
```bash
cd frontend
npm run dev
```

Para correr las pruebas del frontend:
```bash
cd frontend
npm run test:unit -- --run
```
