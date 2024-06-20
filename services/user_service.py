from core.hashing import Hasher
from db.models.user import Role
from db.repository.user_repository import create_new_user, get_user_by_email
from db.session import get_db
from fastapi import APIRouter, Depends, Request, Response, status, HTTPException

from sqlalchemy.orm import Session
from core.config import settings
from schemas.token import Token
from jose import JWTError, jwt
from typing import Any, Dict, List, Optional, Union
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.exceptions import HTTPException
from fastapi.openapi.models import OAuth2 as OAuth2Model
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security.base import SecurityBase
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED


class OAuth2Cookie(SecurityBase):
    def __init__(
        self,
        *,
        flows: Union[OAuthFlowsModel, Dict[str, Dict[str, Any]]] = OAuthFlowsModel(),
        scheme_name: Optional[str] = None,
        description: Optional[str] = None,
        auto_error: bool = True,
    ):
        self.model = OAuth2Model(flows=flows, description=description)
        self.scheme_name = scheme_name or self.__class__.__name__
        self.auto_error = auto_error

    async def __call__(self, request: Request) -> Optional[str]:
        authorization = request.cookies.get("token")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED, detail="Not authenticated"
                )
            else:
                return None
        return param


cookie_auth_schema = OAuth2Cookie(
    description="Cần cookie để auth", scheme_name="Bearer"
)


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_user_from_cookie(
    token: str = Depends(cookie_auth_schema), db: Session = Depends(get_db)
):

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(email, db)
    if user is None:
        raise credentials_exception
    return user
