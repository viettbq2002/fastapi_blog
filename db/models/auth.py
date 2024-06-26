from pydantic import BaseModel
from core.config import settings
from typing import Optional

class JwtToken(BaseModel):
    sub: str
    role: str
    iss: str = settings.JWT_ISSUER
    aud: str = settings.JWT_AUDIENCE
