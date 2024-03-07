from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from starlette.responses import JSONResponse
from src.database.connection import Session
from src.database.models import UserResponse, UserUpdate
from src.database.schema import User

user_router_extra = APIRouter(tags=["users_extra"], prefix="/users")


@user_router_extra.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int) -> JSONResponse:
    """
    Retrieve a User by ID.

    Path Parameters:
      - **user_id**: ID of the user.

    Returns:
      - 200 OK: If the user with the provided ID is found.
      - 404 Not Found: If the user with the provided ID does not exist.
    """
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
            message="Users found successfully",
            data=user_list,
            status_code=status.HTTP_200_OK,
        )

        return JSONResponse(content=response.dict(), status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )


@user_router_extra.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_data: UserUpdate, request: Request, user_id: int
) -> JSONResponse:
    """
    Update a User.

    Body Param:
      - **name**: Name of the user.(optional)
      - **email**: Email of the user.(optional)
      - **phone_number**: Phone number of the user.(optional)
      - **password**: Password of the user.(optional)

    Returns:
      - 200 OK: If the user is successfully updated.
      - 404 Not Found: If the user with the provided ID does not exist.
    """

    print(user_id, "this is user id")
    session = Session()
    data = await request.json()

    email = data.get("email")
    phone_number = data.get("phone_number")
    name = data.get("name")
    password = data.get("password")

    user = session.query(User).filter(User.id == user_id).first()
    if user:
        if email is not None:
            user.email = email
        if name is not None:
            user.name = name
        if password is not None:
            user.password = password
        if phone_number is not None:
            user.phone_number = phone_number
        session.commit()
        session.refresh(user)
        print(type(user))

        user_list = [
            {
                "user_name": user.name,
                "email": user.email,
                "phone_number": user.phone_number,
            }
        ]

        print(type(user_list))

        response = UserResponse(
            success=True,
            message="Users updated successfully",
            data=user_list,
            status_code=status.HTTP_200_OK,
        )

        print(response)

        return JSONResponse(content=response.dict(), status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )


@user_router_extra.delete("/{user_id}")
async def delete_user(user_id: int) -> JSONResponse:
    """
    Delete a User.

    Returns:
      - 200 OK: If the user is successfully deleted.
      - 404 Not Found: If the user with the provided ID does not exist.
    """
    session = Session()
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        session.delete(user)
        session.commit()
        return JSONResponse(
            content={"message": "User deleted successfully"},
            status_code=status.HTTP_200_OK,
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
