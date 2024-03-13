from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from src.common.configuration import (ACCESS_TOKEN_EXPIRE_DAYS, ALGORITHM,
                                      SECRET_KEY)
from src.database.models import TokenData


def create_access_token(user_id: int, expires_delta: timedelta | None = None):
    to_encode = {"user_id": user_id}
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=7)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        bearer_token = token.split(' ')[1]
        payload = jwt.decode(bearer_token, SECRET_KEY, algorithms=[ALGORITHM])

        print(payload)
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        return user_id  
    except JWTError:
        raise credentials_exception
