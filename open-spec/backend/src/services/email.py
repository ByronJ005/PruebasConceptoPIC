from fastapi import BackgroundTasks
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from backend.src.core.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.SMTP_USER,
    MAIL_PASSWORD=settings.SMTP_PASSWORD,
    MAIL_FROM=settings.EMAILS_FROM_EMAIL,
    MAIL_PORT=settings.SMTP_PORT,
    MAIL_SERVER=settings.SMTP_HOST,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=False
)

class EmailService:
    @staticmethod
    def send_password_reset(background_tasks: BackgroundTasks, to_email: str, reset_url: str):
        html = f"""
        <html>
        <body>
            <h2>Restablecer Contraseña - TerminalLoja</h2>
            <p>Hola,</p>
            <p>Recibimos una solicitud para restablecer la contraseña de tu cuenta en TerminalLoja.</p>
            <p>Haz clic en el enlace de abajo para continuar:</p>
            <p><a href="{reset_url}">{reset_url}</a></p>
            <p>Este enlace expirará en 1 hora.</p>
            <p>Si no realizaste esta solicitud, puedes ignorar este correo de forma segura.</p>
        </body>
        </html>
        """
        message = MessageSchema(
            subject="Restablecer Contraseña - TerminalLoja",
            recipients=[to_email],
            body=html,
            subtype=MessageType.html
        )
        fm = FastMail(conf)
        background_tasks.add_task(fm.send_message, message)
