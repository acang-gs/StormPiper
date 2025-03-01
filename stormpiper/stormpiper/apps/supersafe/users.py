import datetime
import logging
import urllib.parse
import uuid
from typing import Any, Optional

import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    CookieTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users.jwt import decode_jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from stormpiper.core import utils
from stormpiper.core.config import settings
from stormpiper.email_helper import email

from .db import User, get_async_session, get_user_db
from .models import Role, UserCreate, UserRead, UserUpdate

logging.basicConfig(level=settings.LOGLEVEL)
logger = logging.getLogger(__name__)


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = settings.SECRET
    verification_token_secret = settings.SECRET
    reset_password_token_lifetime_seconds = 3600
    verification_token_lifetime_seconds = 3600

    async def on_after_register(
        self, user: User, request: Optional[Request] = None
    ) -> None:
        if request is None:  # pragma: no cover
            return

        logger.info(f"User {user.id} has registered.")

        setattr(request, "_email_template", "welcome_verify")

        await self.request_verify(user=user, request=request)

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ) -> None:
        if request is None:  # pragma: no cover
            return

        client = utils.rgetattr(request, "app.sessions", None).get(
            "user_email_session", None
        )

        expires_at = (
            max(
                datetime.datetime.utcnow(),
                datetime.datetime.utcnow()
                + datetime.timedelta(
                    seconds=self.reset_password_token_lifetime_seconds
                ),
            )
            .replace(tzinfo=datetime.timezone.utc)
            .isoformat()
        )

        query = urllib.parse.urlencode({"token": token, "expires_at": expires_at})
        reset_url = request.url_for("home") + f"/reset?{query}"

        await email.send_email_to_user(
            template="reset_password",
            client=client,
            email=user.email,
            name=user.first_name,
            token=token,
            reset_url=reset_url,
        )

        logger.info(f"User {user.id} forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ) -> None:
        if request is None:  # pragma: no cover
            return

        client = utils.rgetattr(request, "app.sessions", None).get(
            "user_email_session", None
        )

        expires_at = (
            max(
                datetime.datetime.utcnow(),
                datetime.datetime.utcnow()
                + datetime.timedelta(seconds=self.verification_token_lifetime_seconds),
            )
            .replace(tzinfo=datetime.timezone.utc)
            .isoformat()
        )

        query = urllib.parse.urlencode({"token": token, "expires_at": expires_at})
        verify_url = request.url_for("home") + f"/verify?{query}"

        logger.info(f"verify url: {verify_url}")
        template = getattr(request, "_email_template", "request_verify")

        await email.send_email_to_user(
            template=template,
            client=client,
            email=user.email,
            name=user.first_name,
            token=token,
            verify_url=verify_url,
        )

        logger.info(
            f"Verification requested for user {user.id}. Verification token: {token}"
        )


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


class BetterBearerTransport(BearerTransport):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_token(self, request: Request) -> str | None:
        token = request.headers.get("Authorization", "").split(" ")[-1]
        if token:  # pragma: no branch
            return token


class BetterCookieTransport(CookieTransport):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_token(self, request: Request) -> str | None:  # pragma: no cover; use Bearer
        token = request.cookies.get(self.cookie_name, "")
        if token:
            return token


bearer_transport = BetterBearerTransport(tokenUrl=settings.BEARER_TOKEN_URL)
cookie_transport = BetterCookieTransport(
    cookie_secure=settings.COOKIE_SECURE,
    cookie_httponly=settings.COOKIE_HTTPONLY,
    cookie_samesite=settings.COOKIE_SAMESITE,
)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.SECRET, lifetime_seconds=settings.JWT_LIFETIME_SECONDS
    )


bearer_backend = AuthenticationBackend(
    name="jwt.bearer",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

cookie_backend = AuthenticationBackend(
    name="jwt.cookie",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager=get_user_manager,
    auth_backends=[bearer_backend, cookie_backend],
)


def current_user_safe(**kwargs):
    async def _get_current_user(
        user: User = Depends(fastapi_users.current_user(**kwargs)),
    ) -> Optional[UserRead]:
        if user:
            return UserRead.from_orm(user)

    return _get_current_user


current_active_user = current_user_safe(active=True, optional=False)
current_active_super_user = current_user_safe(
    active=True, superuser=True, optional=False
)


def check_role(min_role: Role = Role.admin):
    async def current_active_user_role(user=Depends(current_active_user)):
        if user.role._q() >= min_role._q():
            return user

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return current_active_user_role


# check if role >= 100
check_admin = check_role(min_role=Role.admin)

# check user has edit rights
check_user_admin = check_role(min_role=Role.user_admin)

# check if role >= 1, i.e., not public
check_reader = check_role(min_role=Role.reader)

# check user has edit rights
check_user = check_role(min_role=Role.editor)


def check_protected_user_patch(field: str, min_role: Role = Role.admin):
    """Check if user is attempting to edit the user role."""

    async def current_active_user_role(
        user_update: UserUpdate,
        current_user=Depends(current_active_user),
        user_db=Depends(get_user_db),
        id: Any = None,
    ) -> UserUpdate:
        data = user_update.dict(exclude_unset=True)

        if field not in data:
            return user_update

        changing_self = True  # assume update is for current user

        other_user_current_role = Role.none
        if id:
            other_user = await user_db.get(id)
            other_user_current_role = getattr(other_user, "role", Role.none)
            changing_self = str(id) == str(current_user.id)

        new_role = user_update.role

        checks = (
            current_user.role._q() >= min_role._q(),
            current_user.role._q() >= new_role._q(),
            current_user.role._q() >= other_user_current_role._q(),
            # if you're changing yourself and you're changing the role attribute, break the check
            not (changing_self and (current_user.role._q() != new_role._q())),
        )

        # prevent users from elevating permissions
        if all(checks):
            return user_update

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return current_active_user_role


check_protect_role_field = check_protected_user_patch(
    field="role", min_role=Role.user_admin
)


def get_token_from_backend(request: Request) -> str | None:

    for be in fastapi_users.authenticator.backends:
        token = be.transport.get_token(request)  # type: ignore
        if token:  # pragma: no branch
            return token

    return None  # pragma: no cover


def check_token(token: str):
    strat = get_jwt_strategy()

    try:
        data = decode_jwt(
            token,
            secret=strat.secret,
            audience=strat.token_audience,
            algorithms=[strat.algorithm],
        )

        return data

    except jwt.PyJWTError as e:  # pragma: no cover
        logger.exception(e)
        return None


def is_valid_token(request: Request) -> bool:
    token = get_token_from_backend(request)
    if token is None:  # pragma: no cover
        return False
    data = check_token(token)
    return bool(data)


async def check_is_valid_token(request: Request):
    isvalid = is_valid_token(request)

    if not isvalid:  # pragma: no cover
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


def validate_uuid4(token: str):
    try:
        uuid.UUID(token, version=4)
        return token
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


async def check_readonly_token(
    token: str = Depends(validate_uuid4),
    db: AsyncSession = Depends(get_async_session),
    min_role: Role = Role.reader,
):
    result = await db.execute(select(User).where(User.readonly_token == token))

    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    if not user.role._q() >= min_role._q():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return token
