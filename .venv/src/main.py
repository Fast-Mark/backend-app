from datetime import timedelta
import os
from typing import Annotated

import pkg_resources

from fastapi import Depends, FastAPI, HTTPException, UploadFile
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import  HTMLResponse
from fastapi.staticfiles import StaticFiles


from starlette.responses import FileResponse 
from starlette.responses import RedirectResponse
    

from src.modules import Token, User, UserInDB, ElementWrapper, UserAutorize
from src.users_db import not_real_db_users
from src.save_table import save_uploaded_file
from src.autorize import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token, create_new_user, get_current_active_user

from src.const import BASE_PATH


app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=pkg_resources.resource_filename(__name__, 'static')), name="static")
# app.include_router(
#     apiRouter,
#     prefix="/api",
# )

@app.get("/api/.*", status_code=404, include_in_schema=False)
def invalid_api():
    return None

@app.get("/.*", include_in_schema=False)
def root():
    return HTMLResponse(pkg_resources.resource_string(__name__, 'static/index.html'))


@app.get('/')
async def create_app(current_user: Annotated[User, Depends(get_current_active_user)]):
    # TODO: здесь еще должная быть проверка на авторизацию пользователя. Если не авторизован, то переадресация на  '/autorization'
    if current_user != None:
        return FileResponse(os.path.join(BASE_PATH, ".venv/src/workspace/index.html"), media_type="text/html")
    else:
        return RedirectResponse(url="/autorization")

@app.get('/start')
async def read_start_page():
    pass

@app.get('/workspace')
async def read_start_page():
    return FileResponse(os.path.join(BASE_PATH, ".venv/src/workspace/index.html"), media_type="text/html")

@app.get('/list-results')
async def read_start_page():
    pass

#  Эта функция просто возвращает страницу входа
@app.get('/autorization')
async def give_autorize_pag():
    return FileResponse(os.path.join(BASE_PATH, ".venv/src/static/index.html"), media_type="text/html")

@app.get('/create-user')
async def create_user(email: str, password: str):
    id = create_new_user(password, email)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": id}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@app.post("/verify-user")
async def verify_token(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user

@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[UserAutorize, Depends()]
) -> Token:
    user = authenticate_user(form_data.email, form_data.password)
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

@app.post('/upload-table')
async def upload_table(current_user: Annotated[User, Depends(get_current_active_user)], file: UploadFile, project_name: str):
    await save_uploaded_file(current_user.username, project_name, file)
    return 

# TODO: в будущем нужно будет сохранять названия существующих проектов пользователя
# @app.get('create-resilt')
# async def create_result(current_user: Annotated[User, Depends(get_current_active_user)], json: ElementWrapper, background: UploadFile, project_name: str):
#     pass
