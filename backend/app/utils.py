from pydantic import BaseModel
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from app.core.database import SessionDep
from app.core.security import settings
from app.core import security
import emails
import jwt
from jinja2 import Template
from jwt.exceptions import InvalidTokenError

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class EmailBase(BaseModel):
    htlm_content: str
    subject: str


def render_email_template(*, template_name: str, context: dict[str, Any]) -> str:
    template_str =(
        Path(__file__).parent / "emails_templates" / "build" / template_name
    ).read_text()
    html_content = Template(template_str).render(context)
    return html_content

def send_email(
    *,
    email_to: str,
    subject: str = "",
    html_content: str = "",
) -> None:
    assert settings.emails_enabled, "no provided configuratio for email variables"
    message = emails.Message(
        subject=subject,
        html=html_content,
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL)
    )
    smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
    if settings.SMTP_TLS:
        smtp_options['tls'] = True
    elif settings.SMTP_SSL:
        smtp_options['ssl'] = True
    if settings.SMTP_USER:
        smtp_options['user'] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options['password'] = settings.SMTP_PASSWORD
    response = message.send(to=email_to, smtp=smtp_options)
    logger.info(f"send email result: {response}")

def generate_test_email(email_to: str) -> EmailBase:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Test email"
    html_content = render_email_template(
        template_name=project_name,
        context={"project_name": settings.PROJECT_NAME, "email": email_to}
    )
    return EmailBase(html_content=html_content, subject=subject)

def generate_reset_password_email(email_to: str, email: str, token: str) -> EmailBase:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Password recovery for user {email}."
    link = f"{settings.FRONTEND_HOST}/reset-password/?token={token}"
    html_content = render_email_template(
        template_name="reset_password.html",
        context={
            "project_name": settings.PROJECT_NAME,
            "username": email,
            "email": email_to,
            "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "link": link                
        },
    )
    return EmailBase(htlm_content=html_content, subject=subject)

def generate_password_reset_token(email: str) -> str:

    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    to_encode = {"sub": email, "nbf": now, "exp": expires}
    jwt_encoded = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=security.ALGORITHM
    )
    return jwt_encoded

def generate_new_account_email(
    email_to: str, username: str, password: str
) -> EmailBase:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - New account for user {username}"
    html_content = render_email_template(
        template_name="new_account.html",
        context={
            "project_name": settings.PROJECT_NAME,
            "username": username,
            "password": password,
            "email": email_to,
            "link": settings.FRONTEND_HOST,
        },
    )
    return EmailBase(html_content=html_content, subject=subject)


def generate_test_email(email_to: str) -> EmailBase:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Test email"
    html_content = render_email_template(
        template_name="test_email.html",
        context={"project_name": settings.PROJECT_NAME, "email": email_to},
    )
    return EmailBase(html_content=html_content, subject=subject)

def verify_password_reset_token(token:str) -> str | None:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=[security.ALGORITHM])
        return str(decoded_token['sub'])
    except InvalidTokenError:
        return None