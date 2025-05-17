import os
from uuid import UUID
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import EmailStr
from dotenv import load_dotenv
from fastapi import UploadFile
from src.account.models import User
from src.account.repositories import UserRepository
from src.core.db import SessionLocal
from src.core.logger import logger
from src.core.exceptions import NotFoundException
from src.event.repositories.ticket import TicketRepository
from src.event.utils import generate_qr_code


env = load_dotenv()


class Envs:
    MAIL_USERNAME: str = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD: str = os.getenv("MAIL_PASSWORD")
    MAIL_FROM: str = os.getenv("MAIL_FROM")
    MAIL_PORT: int = os.getenv("MAIL_PORT")
    MAIL_SERVER: str = os.getenv("MAIL_SERVER")
    MAIL_FROM_NAME: str = os.getenv("MAIL_FROM_NAME")
    MAIL_STARTTLS: bool = os.getenv("MAIL_STARTTLS")
    MAIL_SSL_TLS: bool = os.getenv("MAIL_SSL_TLS")
    USE_CREDENTIALS: bool = os.getenv("USE_CREDENTIALS")
    VALIDATE_CERTS: bool = os.getenv("VALIDATE_CERTS")


email_env = Envs()

conf = ConnectionConfig(
    MAIL_USERNAME=email_env.MAIL_USERNAME,
    MAIL_PASSWORD=email_env.MAIL_PASSWORD,
    MAIL_FROM=email_env.MAIL_FROM,
    MAIL_PORT=email_env.MAIL_PORT,
    MAIL_SERVER=email_env.MAIL_SERVER,
    MAIL_FROM_NAME=email_env.MAIL_FROM_NAME,
    MAIL_STARTTLS=email_env.MAIL_STARTTLS,
    MAIL_SSL_TLS=email_env.MAIL_SSL_TLS,
    USE_CREDENTIALS=email_env.USE_CREDENTIALS,
    VALIDATE_CERTS=email_env.VALIDATE_CERTS
)


def create_attachments(reservation_id):
    with SessionLocal() as db:
        tickets_data = TicketRepository.get_tickets_by_reservation(
            reservation_id=reservation_id,
            db=db
        )
        attachments = []
        for i, ticket in enumerate(tickets_data):
            ticket_info = f"Status ID: {ticket.status_id}, Event ID: {ticket.event_id}"

            # Generate the QR code for each ticket
            qr_image = generate_qr_code(ticket_info)

            # Prepare UploadFile instances
            upload_file = UploadFile(
                file=qr_image,
                filename=f"ticket_{i+1}.png"
            )
            attachments.append(upload_file)
        return attachments


def get_user_email(user_id: UUID) -> str:
    with SessionLocal() as db:
        user = UserRepository.get_user_by_id(db, user_id)
        if not user:
            raise NotFoundException("User with a given id not found.")

        return user.email


async def send_email(user_id: UUID, reservation_id) -> dict[str, str]:
    attachements = create_attachments(reservation_id)
    recipient: EmailStr = get_user_email(user_id)
    message = MessageSchema(
        subject="Test Email",
        recipients=[recipient],
        attachments=attachements,
        body="This is a test email from FastAPI!",
        subtype=MessageType.plain,
    )

    fm = FastMail(conf)

    await fm.send_message(message)
    logger.info(f"email has been sent to {recipient}")
    return {"message": "email has been sent"}
