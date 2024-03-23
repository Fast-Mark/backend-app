from datetime import timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, UploadFile
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

from src.modules import Token, User, UserInDB
from src.users_db import not_real_db_users
from src.tableManager import save_uploaded_file
from src.autorize import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token, create_new_user, get_current_active_user



app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def create_app():
    return {"hello": "world"}

@app.get('/start')
async def read_start_page():
    pass

@app.get('/workspace')
async def read_start_page():
    pass

@app.get('/result')
async def read_start_page():
    pass

@app.get('/list-results')
async def read_start_page():
    pass


@app.get('/create-user')
async def create_user(username: str, email: str, password: str):
    create_new_user(username, password, email)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@app.post("/verify-user")
async def verify_token(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user

@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")



# TODO: сохранять таблицу и шрифт.
# пока что можно просто создаватоь папку пользователя и добавлять туда

@app.post('/file/upload-table')
async def upload_table(user_name: str, file: UploadFile):
    result = await save_uploaded_file(user_name, file)
    return result


@app.get("/posts")
async def give_posts():
    return "hello world!"