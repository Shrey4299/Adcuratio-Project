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


# @user_router.get("/sample/")
# async def read_items(
#     shrey_header: Optional[str] = Header(None),
#     my_cookie_sample: Optional[str] = Cookie(None),
# ):
#     return {"User-Agent": shrey_header, "Cookie": my_cookie_sample}
