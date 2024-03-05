from typing import Annotated, Optional
from starlette.responses import JSONResponse
from src.database.schema import User
from src.database.models import UserSignUp, UserSignIn, UserResponse
from fastapi import APIRouter, Cookie, HTTPException, Header, status, Request, Query
from src.database.connection import Session
from fastapi.encoders import jsonable_encoder

user_router = APIRouter(tags=["users"], prefix="/users")


@user_router.get("/", response_model=UserResponse)
async def get_user() -> JSONResponse:
    """
    Retrieve a User by Name or Phone Number.

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


@user_router.get("/by-name", response_model=UserResponse)
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
async def create_user(user_data: UserSignUp) -> JSONResponse:
    """
    Sign Up a User.

    Body Param:
     - **name**: Name of the user.
     - **email**: Email of the user.
     - **phone_number**: Phone number of the user.
     - **password**: Password of the user.

    Returns:
      - 201 Created: If the user is successfully signed up.
      - 409 Conflict: If the user with the provided email or phone number already exists.
    """
    session = Session()

    user_with_email = session.query(User).filter(User.email == user_data.email).first()
    if user_with_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )

    user_with_phone = (
        session.query(User).filter(User.phone_number == user_data.phone_number).first()
    )
    if user_with_phone:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this phone number already exists",
        )

    # Create a new user
    user = User(**user_data.dict())
    session.add(user)
    session.commit()
    session.refresh(user)

    print(type(user))

    user_list = [{"user_name": user.name, "email": user.email, "phone_number": user.phone_number}]

    print(type(user_list))

    response = UserResponse(
        success=True,
        message="Users created successfully",
        data=user_list,
        status_code=status.HTTP_200_OK,
    )

    print(response)

    return JSONResponse(content=response.dict(), status_code=status.HTTP_200_OK)


@user_router.post("/signin")
async def signin_user(user_data: UserSignIn):
    """
    Sign In a User.

    Body Param:
    - **email**: Email of the user.
    - **password**: Password of the user.

    Returns:
      - 200 OK: If the user is successfully signed in.
      - 401 Unauthorized: If the password is incorrect.
      - 404 Not Found: If the user with the provided email does not exist.
    """
    session = Session()
    user = session.query(User).filter(User.email == user_data.email).first()
    if user:
        if user.password == user_data.password:
            print(type(user))

            user_list = [
                {"user_name": user.name, "email": user.email, "phone_number": user.phone_number}
            ]

            print(type(user_list))

            response = UserResponse(
                success=True,
                message="Users logged in  successfully",
                data=user_list,
                status_code=status.HTTP_200_OK,
            )

            print(response)

            return JSONResponse(content=response.dict(), status_code=status.HTTP_200_OK)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
