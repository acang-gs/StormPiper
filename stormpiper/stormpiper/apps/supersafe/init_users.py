import contextlib

from fastapi_users.exceptions import UserAlreadyExists

from stormpiper.core.config import settings

from .db import get_async_session, get_user_db
from .models import UserCreate
from .users import get_user_manager

get_async_session_context = contextlib.asynccontextmanager(get_async_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_user(email: str, password: str, is_superuser: bool = False, **kwargs):
    try:
        print(f"trying to create user {email}")
        async with get_async_session_context() as session:
            async with get_user_db_context(session) as user_db:
                async with get_user_manager_context(user_db) as user_manager:
                    user = await user_manager.create(
                        UserCreate(
                            email=email,
                            password=password,
                            is_superuser=is_superuser,
                            **kwargs,
                        )
                    )
                    print(f"User created {user}")
    except UserAlreadyExists:
        print(f"User {email} already exists")


async def create_admin():
    return await create_user(
        email="admin@geosyntec.com",
        password=settings.ADMIN_ACCOUNT_PASSWORD,  # type: ignore
        is_superuser=True,
    )


async def create_public():
    return await create_user(
        email="public@nowhere.com",
        password="unsafe_password",
    )


async def create_all():
    await create_admin()
    await create_public()


def main():
    import asyncio
    import platform

    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(create_all())


if __name__ == "__main__":
    main()
