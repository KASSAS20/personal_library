from fastapi import Depends, HTTPException
from app.router import router
from app.components.auth import oauth2
from typing import Annotated

router = router


# Тестовый роутер для демонстрации работы OAuth2
@router.get("/test")
async def test(token: Annotated[oauth2, Depends()]):
    return token