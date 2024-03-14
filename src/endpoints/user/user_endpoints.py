from operator import or_
from typing import Annotated

from fastapi import (APIRouter, Depends, Header, HTTPException, Query, Request,
                     status)
from fastapi.security import OAuth2PasswordBearer
from starlette.responses import JSONResponse

from src.auth.hashing import Hash
from src.auth.token_access import create_access_token, verify_token
from src.database.connection import Session
from src.database.models import UserResponse, UserSignIn, UserSignUp
from src.database.schema import User

user_router = APIRouter(tags=["users"], prefix="/users")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@user_router.get(
    "/", response_model=UserResponse
)
async def get_user(
    current_user: Annotated[User, Depends(verify_token)]
) -> JSONResponse:
    """
    Retrieve a User by Name or Phone Number.

    Query Param:
    - None

    Parameters:
    - None

    Returns:
      - 200 OK: List of users.
      - 404 Not Found: If no user is found matching the query parameters.
    """
    
    session = Session()
    query = session.query(User)

    users = query.all()

    if users:
        user_list = []
        for user in users:
            user_dict = {
                "id": user.id,
                "name": user.name,
                "phone_number": user.phone_number,
            }
            user_list.append(user_dict)

        response = UserResponse(
            success=True,
            message="Users found",
            data=user_list,
            status_code=status.HTTP_200_OK,
        )

        return JSONResponse(content=response.dict(), status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Users not found"
        )


@user_router.get("/by-detail", response_model=UserResponse)
async def get_user_by_name(
    name: str = Query(None, description="user name"),
    phone_number: str = Query(None, description="user phone number"),
) -> JSONResponse:
    """
    Retrieve a User by Name or Phone Number.

    Query Param:
     - **name**: Name of the user (optional).
     - **phone_number**: Phone number of the user (optional).

    Returns:
      - 200 OK: List of users matching the query parameters.
      - 404 Not Found: If no user is found matching the query parameters.
    """
    session = Session()
    query = session.query(User)
    if name:
        query = query.filter(User.name == name)
    if phone_number:
        query = query.filter(User.phone_number == phone_number)
    users = query.all()

    if users:
        user_list = []
        for user in users:
            user_dict = {
                "id": user.id,
                "name": user.name,
                "phone_number": user.phone_number,
            }
            user_list.append(user_dict)

        response = UserResponse(
            success=True,
            message="Users found",
            data=user_list,
            status_code=status.HTTP_200_OK,
        )

        return JSONResponse(content=response.dict(), status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Users not found"
        )


@user_router.post("/signup", response_model=UserResponse)
async def create_user(user_data: UserSignUp, request: Request) -> JSONResponse:
    session = Session()

    data = await request.json()
    name = data.get("name")
    email = data.get("email")
    phone_number = data.get("phone_number")
    password = data.get("password")

    user_with_email = session.query(User).filter(User.email == email).first()
    if user_with_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )

    user_with_phone = (
        session.query(User).filter(User.phone_number == phone_number).first()
    )
    if user_with_phone:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this phone number already exists",
        )

    hashed_password = Hash.bcrypt(password)  # Hash the password

    # Create a new user with the hashed password
    user = User(
        name=name,
        email=email,
        phone_number=phone_number,
        password=hashed_password,
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    user_list = [
        {"user_name": user.name, "email": user.email, "phone_number": user.phone_number}
    ]

    response = UserResponse(
        success=True,
        message="User created successfully",
        data=user_list,
        status_code=status.HTTP_201_CREATED,
    )

    return JSONResponse(content=response.dict(), status_code=status.HTTP_201_CREATED)


@user_router.post("/signin", response_model=UserResponse)
async def signin_user(signin_data: UserSignIn, request: Request) -> JSONResponse:
    session = Session()

    data = await request.json()
    email = data.get("email")
    phone_number = data.get("phone_number")
    password = data.get("password")

    user = (
        session.query(User)
        .filter(or_(User.email == email, User.phone_number == phone_number))
        .first()
    )
    if user:
        if Hash.verify(user.password, password):
            jwt_token = create_access_token(user.id)

            user_data = {"jwt": jwt_token}
            response = UserResponse(
                success=True,
                message="User signed in successfully",
                data=[user_data],
                status_code=status.HTTP_200_OK,
            )
            return JSONResponse(content=response.dict(), status_code=status.HTTP_200_OK)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email, phone number, or password",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )


@user_router.get("/get-me", response_model=UserResponse)
async def get_user(user_id: Annotated[User, Depends(verify_token)]) -> JSONResponse:
    """
    Retrieve a User by ID encoded in JWT token.

    Returns:
      - 200 OK: If the user with the provided ID is found.
      - 401 Unauthorized: If the JWT token is invalid or missing.
      - 404 Not Found: If the user with the provided ID does not exist.
    """



    if user_id is not None:
        session = Session()
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            user_list = [
                {
                    "user_name": user.name,
                    "email": user.email,
                    "phone_number": user.phone_number,
                }
            ]

            response = UserResponse(
                success=True,
                message="User found successfully",
                data=user_list,
                status_code=status.HTTP_200_OK,
            )

            return JSONResponse(content=response.dict(), status_code=status.HTTP_200_OK)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )


@user_router.get("/sample/")
async def read_items(token: Annotated[str | None, Header()] = None):
    print(token)
    return {"token": token}
