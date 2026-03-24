from contextlib import asynccontextmanager
import logging

from fastapi import Depends, FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .config import get_settings
from .database import Base, engine, get_db
from .mailer import EmailDeliveryError, send_application_email
from .models import ApplicationSubmission
from .schemas import ApplicationSubmissionCreate, ApplicationSubmissionResponse, HealthResponse


settings = get_settings()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
def healthcheck() -> HealthResponse:
    return HealthResponse(status="ok")


@app.post(
    "/api/applications",
    response_model=ApplicationSubmissionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_application(
    payload: ApplicationSubmissionCreate,
    db: Session = Depends(get_db),
) -> ApplicationSubmissionResponse:
    submission = ApplicationSubmission(
        name=payload.name,
        email=payload.email,
        phone=payload.phone,
        organization=payload.organization,
        position=payload.position,
        group_name=payload.group_name,
        motive=payload.motive,
        career=payload.career,
        start_date=payload.start_date,
        available_days=payload.available_days,
        note=payload.note,
        agreed_to_privacy=payload.agreed_to_privacy,
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)

    email_sent = True
    email_error = None

    try:
        send_application_email(payload, settings)
    except EmailDeliveryError as exc:
        email_sent = False
        email_error = str(exc)
        logger.warning("Application email delivery failed: %s", exc)

    return ApplicationSubmissionResponse(
        id=submission.id,
        name=submission.name,
        email=submission.email,
        group_name=submission.group_name,
        created_at=submission.created_at,
        email_sent=email_sent,
        email_error=email_error,
    )


@app.get("/")
def read_root() -> dict[str, str]:
    return {
        "name": settings.app_name,
        "environment": settings.environment,
        "healthcheck": "/health",
        "submit_endpoint": "/api/applications",
    }
