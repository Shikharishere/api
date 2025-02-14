"""
    User validators.
"""

from validate_email import validate_email


from app.config import get_settings
from app.database import crud
from app.services.api.errors import ApiErrorCode, ApiErrorException
from app.database.models.user import User
from app.services.passwords import check_password


def validate_signup_fields(db, username: str, email: str, password: str) -> None:
    """Validates that all fields passes signup base validation, or raises API error if not."""

    settings = get_settings()

    # Check email is not taken.
    if crud.user.email_is_taken(db=db, email=email):
        raise ApiErrorException(
            ApiErrorCode.AUTH_EMAIL_TAKEN, "Given email is already taken!"
        )

    # Check username is not taken.
    if crud.user.username_is_taken(db=db, username=username):
        raise ApiErrorException(
            ApiErrorCode.AUTH_USERNAME_TAKEN, "Given username is already taken!"
        )

    # Validate email.
    if settings.signup_validate_email and not validate_email(
        email, verify=False
    ):  # TODO.
        raise ApiErrorException(ApiErrorCode.AUTH_EMAIL_INVALID, "Email invalid!")

    # Check username.
    if len(username) <= 4:
        raise ApiErrorException(
            ApiErrorCode.AUTH_USERNAME_INVALID, "Username should be longer than 4!"
        )
    if len(username) > 16:
        raise ApiErrorException(
            ApiErrorCode.AUTH_USERNAME_INVALID, "Username should be shorten than 16!"
        )
    if settings.signup_username_reject_nonalpha and not username.isalpha():
        raise ApiErrorException(
            ApiErrorCode.AUTH_USERNAME_INVALID,
            "Username should only contain alphabet characters!",
        )
    if settings.signup_username_reject_uppercase and not username.islower():
        raise ApiErrorException(
            ApiErrorCode.AUTH_USERNAME_INVALID,
            "Username should only contain lowercase characters!",
        )

    # Check password.
    if len(password) <= 5:
        raise ApiErrorException(
            ApiErrorCode.AUTH_PASSWORD_INVALID, "Password should be longer than 5!"
        )
    if len(password) > 64:
        raise ApiErrorException(
            ApiErrorCode.AUTH_PASSWORD_INVALID, "Password should be shorten than 64!"
        )


def validate_signin_fields(user: User, password: str) -> None:
    """Validates that all fields passes signin base validation, or raises API error if not."""

    if not user or not check_password(password=password, hashed_password=user.password):
        raise ApiErrorException(
            ApiErrorCode.AUTH_INVALID_CREDENTIALS,
            "Invalid credentials for authentication.",
        )
