from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class ApplicationSubmissionCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: str = Field(..., min_length=1, max_length=50)
    organization: str = Field(default="Not provided", max_length=255)
    position: str = Field(default="Not provided", max_length=255)
    group_name: str = Field(..., min_length=1, max_length=255)
    motive: str = Field(default="None")
    career: str = Field(default="None")
    start_date: str = Field(default="Not provided", max_length=100)
    available_days: str = Field(default="Not provided", max_length=255)
    note: str = Field(default="None")
    agreed_to_privacy: bool

    @field_validator(
        "name",
        "phone",
        "organization",
        "position",
        "group_name",
        "motive",
        "career",
        "start_date",
        "available_days",
        "note",
        mode="before",
    )
    @classmethod
    def strip_strings(cls, value: str) -> str:
        if isinstance(value, str):
            return value.strip()
        return value

    @field_validator("agreed_to_privacy")
    @classmethod
    def ensure_privacy_consent(cls, value: bool) -> bool:
        if not value:
            raise ValueError("Privacy consent is required.")
        return value


class ApplicationSubmissionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    group_name: str
    created_at: datetime
    email_sent: bool
    email_error: str | None = None


class HealthResponse(BaseModel):
    status: str
