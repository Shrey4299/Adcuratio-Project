from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from starlette.responses import JSONResponse

from src.database.connection import Session
from src.database.models import UserResponse, UserSignIn, UserSignUp
from src.database.schema import User

user_router = APIRouter(tags=["users"], prefix="/users")


async def method_finder(request: Request):
    method_name = request.method
    return method_name



@user_router.get("/", response_model=UserResponse)
async def get_user(
    api_method: Annotated[dict, Depends(method_finder)]
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
    print(api_method + ' : this is the api method')
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

    data = await request.json()
    email = data.get("email")
    phone_number = data.get("phone_number")

    print(data)

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

    # Create a new user
    user = User(**data)
    session.add(user)
    session.commit()
    session.refresh(user)

    print(type(user))

    user_list = [
        {"user_name": user.name, "email": user.email, "phone_number": user.phone_number}
    ]

    print(type(user_list))

    response = UserResponse(
        success=True,
        message="Users created successfully",
        data=user_list,
        status_code=status.HTTP_200_OK,
    )

    print(response)

    return JSONResponse(content=response.dict(), status_code=status.HTTP_200_OK)


@user_router.post("/signin", response_model=UserResponse)
async def signin_user(user_data: UserSignIn, request: Request) -> JSONResponse:
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
    # Extracting email and password from the request body
    data = await request.json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email and password are required",
        )

    session = Session()
    user = session.query(User).filter(User.email == email).first()
    if user:
        if user.password == password:
            user_list = [
                {
                    "user_name": user.name,
                    "email": user.email,
                    "phone_number": user.phone_number,
                }
            ]

            response = UserResponse(
                success=True,
                message="Users logged in successfully",
                data=user_list,
                status_code=status.HTTP_200_OK,
            )

            return JSONResponse(content=response.dict(), status_code=status.HTTP_200_OK)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
