import json
from urllib import error, request

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
    if not settings.email_configured:
        raise EmailDeliveryError("Resend settings are not configured.")

    body = {
        "from": settings.mail_from,
        "to": [settings.admin_email],
        "subject": f"[Advisory Application] {payload.name} / {payload.group_name}",
        "text": _build_plain_text(payload),
        "reply_to": payload.email,
    }
    data = json.dumps(body).encode("utf-8")
    req = request.Request(
        settings.resend_api_url,
        data=data,
        headers={
            "Authorization": f"Bearer {settings.resend_api_key}",
            "Content-Type": "application/json",
            "User-Agent": "citizenparticipation-backend/1.0",
        },
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=20) as response:
            status_code = getattr(response, "status", response.getcode())
            if status_code >= 400:
                raise EmailDeliveryError(f"Resend API request failed with status {status_code}.")
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise EmailDeliveryError(
            f"Resend API request failed with status {exc.code}: {detail}"
        ) from exc
    except error.URLError as exc:
        raise EmailDeliveryError(f"Resend API network error: {exc.reason}") from exc
    except Exception as exc:
        raise EmailDeliveryError(f"Failed to deliver the application email: {exc}") from exc
