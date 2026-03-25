from email.message import EmailMessage
import smtplib

from .config import Settings
from .schemas import ApplicationSubmissionCreate


class EmailDeliveryError(RuntimeError):
    pass


def _build_plain_text(payload: ApplicationSubmissionCreate) -> str:
    fields = [
        ("Name", payload.name),
        ("Email", payload.email),
        ("Phone", payload.phone),
        ("Organization/School", payload.organization),
        ("Position/Grade", payload.position),
        ("Application Group", payload.group_name),
        ("Motivation", payload.motive),
        ("Relevant Experience", payload.career),
        ("Available Start Date", payload.start_date),
        ("Available Days", payload.available_days),
        ("Note", payload.note),
        ("Privacy Consent", "Agreed"),
    ]
    return "\n".join(f"{label}: {value}" for label, value in fields)


def send_application_email(payload: ApplicationSubmissionCreate, settings: Settings) -> None:
    if not settings.smtp_configured:
        raise EmailDeliveryError("SMTP settings are not configured.")

    message = EmailMessage()
    message["Subject"] = f"[Advisory Application] {payload.name} / {payload.group_name}"
    message["From"] = settings.mail_from
    message["To"] = settings.admin_email
    message["Reply-To"] = payload.email
    message.set_content(_build_plain_text(payload))

    try:
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=20) as smtp:
            if settings.smtp_use_tls:
                smtp.starttls()
            smtp.login(settings.smtp_username, settings.smtp_password)
            smtp.send_message(message)
    except Exception as exc:
        raise EmailDeliveryError(f"Failed to deliver the application email: {exc}") from exc
