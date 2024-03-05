from pydantic import BaseModel, EmailStr, Field
from typing import Any


class UserSignUp(BaseModel):
    name: str = Field(description="The name of the user.")
    password: str = Field(description="The password of the user.")
    email: EmailStr = Field(description="The email address of the user.")
    phone_number: str | None = Field(None, description="The phone number of the user.")


class UserSignIn(BaseModel):
    password: str = Field(description="The password of the user.")
    email: EmailStr = Field(description="The email address of the user.")


class UserUpdate(BaseModel):
    name: str | None = Field(None, description="The updated name of the user.")
    password: str | None = Field(None, description="The updated password of the user.")
    email: EmailStr | None = Field(
        None, description="The updated email address of the user."
    )
    phone_number: str | None = Field(
        None, description="The updated phone number of the user."
    )


class UserResponse(BaseModel):
    success: bool = Field(description="Indicates if the operation was successful.")
    message: str = Field(description="Message describing the result of the operation."
    )
    data: Any = Field(description="Data associated with the operation result.")
    status_code: int = Field(description="HTTP status code of the response.")
