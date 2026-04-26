import urllib.parse
import aiohttp
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ....config import settings
from ...models import User


GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
GITHUB_USER_URL = "https://api.github.com/user"
GITHUB_AUTH_URL = "https://github.com/login/oauth/authorize"


def generate_oauth_redirect_uri() -> str:
    params = {
        "client_id": settings.OAUTH_GITHUB_CLIENT_ID,
        "redirect_uri": settings.OAUTH_GITHUB_REDIRECT_URI,
        "scope": "read:user user:email",
    }
    return f"{GITHUB_AUTH_URL}?{urllib.parse.urlencode(params)}"


async def exchange_code_for_token(code: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            GITHUB_TOKEN_URL,
            data={
                "client_id": settings.OAUTH_GITHUB_CLIENT_ID,
                "client_secret": settings.OAUTH_GITHUB_CLIENT_SECRET,
                "code": code,
                "redirect_uri": settings.OAUTH_GITHUB_REDIRECT_URI,
            },
            headers={"Accept": "application/json"}
        ) as res:
            payload = await res.json()
            if res.status != 200 or "error" in payload:
                raise HTTPException(
                    status_code=400, 
                    detail=f"GitHub OAuth error: {payload.get('error_description', 'Unknown error')}"
                )
            return payload["access_token"]


async def get_user_info(token: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            GITHUB_USER_URL,
            headers={"Authorization": f"Bearer {token}"}
        ) as res:
            if res.status != 200:
                raise HTTPException(status_code=401, detail="Failed to fetch GitHub user info")
            return await res.json()


async def get_or_create_github_user(db: AsyncSession, github_info: dict) -> User:
    github_id = str(github_info["id"])
    email = github_info.get("email")
    
    result = await db.execute(select(User).where(User.github_id == github_id))
    user = result.scalar_one_or_none()
    
    if user:
        return user

    if email:
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()

    if user:
        user.github_id = github_id
        if not user.picture:
            user.picture = github_info.get("avatar_url")
        await db.commit()
        await db.refresh(user)
        return user

    new_user = User(
        github_id=github_id,
        email=email or f"{github_info['login']}@github.com",
        name=github_info.get("name") or github_info["login"],
        picture=github_info.get("avatar_url"),
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return new_user
