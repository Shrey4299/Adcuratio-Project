from typing import Annotated, Optional
from starlette.responses import JSONResponse
from src.database.schema import User
from src.database.models import UserSignUp, UserSignIn, UserResponse
from fastapi import APIRouter, Cookie, HTTPException, Header, status, Request, Query
from src.database.connection import Session
from fastapi.encoders import jsonable_encoder

user_router = APIRouter(tags=["users"], prefix="/users")


@user_router.get("/sample/")
async def read_items(ads_id: Optional[str] = Cookie(None)):
    return {"ads_id": ads_id}


# async def read_items(
#     shrey_header: Optional[str] = Header(None), my_cookie_sample: Optional[str] = Cookie(None)
# ):
#     return {"User-Agent": shrey_header, "Cookie": my_cookie_sample}


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
                # Add more fields as needed
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
        raise HTTPException(status_code=404, detail="Users not found")


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
                # Add more fields as needed
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
        raise HTTPException(status_code=404, detail="Users not found")


@user_router.post("/signup")
async def create_user(user_data: UserSignUp):
    """
    Sign Up a User.

    Body Param:
     - **name**: Name of the user.
     - **email**: Email of the user.
     - **password**: Password of the user.

    Returns: 201 Created
      - If the user is successfully signed up.

    Returns: 409 Conflict
      - If the user with the provided email already exists.
    """
    session = Session()
    user = session.query(User).filter(User.email == user_data.email).first()
    if user:
        raise HTTPException(
            status_code=409, detail="User with this email already exists"
        )
    else:
        user = User(**user_data.dict())
        session.add(user)
        session.commit()
        session.refresh(user)
        return JSONResponse(
            content={"message": "success", "data": "user created successfully"},
            status_code=status.HTTP_201_CREATED,
        )


@user_router.post("/signin")
async def signin_user(user_data: UserSignIn):
    """
    Sign In a User.

    Body Param:
    - **email**: Email of the user.
    - **password**: Password of the user.

    Returns: 200 OK
    - If the user is successfully signed in.

    Returns: 401 Unauthorized
    - If the password is incorrect.

    Returns: 404 Not Found
    - If the user with the provided email does not exist.
    """

    session = Session()
    user = session.query(User).filter(User.email == user_data.email).first()
    if user:
        if user.password == user_data.password:
            return user
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )


# @app.get('/user/{user_id}', response_model=User)
# async def get_user(user_id: int) -> JSONResponse:
#     session = Session()
#     user = session.query(DBUser).filter(DBUser.id == user_id).first()
#     if user:
#         return JSONResponse(content=user.dict(), status_code=status.HTTP_200_OK )
#     else:
#         raise HTTPException(status_code=404, detail="User not found")


# @app.get('/user/', response_model=User)
# async def get_user(name: str = None, phone_number: str = None):
#     session = Session()
#     query = session.query(DBUser)
#     if name:
#         query = query.filter(DBUser.name == name)
#     if phone_number:
#         query = query.filter(DBUser.phone_number == phone_number)
#     user = query.first()
#     if user:
#         return user
#     else:
#         raise HTTPException(status_code=404, detail="User not found")


# @app.put('/user/{user_id}', response_model=User)
# async def update_user(user_id: int, email: Optional[str] = None, password: Optional[str] = None, phone_number: Optional[str] = None, name: Optional[str] = None):
#     session = Session()
#     user = session.query(DBUser).filter(DBUser.id == user_id).first()
#     if user:
#         if email is not None:
#             user.email = email
#         if name is not None:
#             user.name = name
#         if password is not None:
#             user.password = password
#         if phone_number is not None:
#             user.phone_number = phone_number
#         session.commit()
#         session.refresh(user)
#         return user
#     else:
#         raise HTTPException(status_code=404, detail="User not found")

# @app.delete('/user/{user_id}')
# async def delete_user(user_id: int):
#     session = Session()
#     user = session.query(DBUser).filter(DBUser.id == user_id).first()
#     if user:
#         session.delete(user)
#         session.commit()
#         return {"message": "User deleted successfully"}
#     else:
#         raise HTTPException(status_code=404, detail="User not found")
