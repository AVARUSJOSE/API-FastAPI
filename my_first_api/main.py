"""importamos libreria fastapi"""
from fastapi import FastAPI, HTTPException, Depends
from users_db.users_db import list_users, User
from users_db.user_root import User_db, UserInDB, fake_users_db
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

app = FastAPI()


@app.get("/")
async def root():
    """definimos funcion y creamos un path"""
    return {"message": "Hello World"}


@app.get("/users/")
async def read_users():
    """funcion que retorna la lista de usuarios completos"""
    return list_users


@app.get("/user/{id}", status_code=200)
async def user(id: int):
    """funcion asincrona con metodo get paraobtener datos desde la API """
    return search_user(id)


# funcion para buscar usuario por su id
def search_user(id: int):
    """funcion que retorna un usuario por su id"""
    for index, users in enumerate(list_users):
        if id == users.id:
            return list_users[index]


@app.post("/user/", status_code=201)
async def add_user(user: User):
    """ingresar nuevo usuario"""
    new_user = user
    list_users.append(new_user)
    return list_users


@app.put("/user/", status_code=202)
async def update_user(user: User):
    """actualizacion de usuarios"""
    for index, saved_user in enumerate(list_users):
        if saved_user.id == user.id:
            list_users[index] = user
    return user


@app.delete("/user/", status_code=202)
async def delete_user(id: int):
    """funcion para eliminar usuario"""
    for index, saved_user in enumerate(list_users):
        if saved_user.id == id:
            del list_users[index]
    return list_users


# seguridad de mi api sencilla

def fake_hash_password(password: str):
    """funcion que genera una password hasheada"""
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    """token"""
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: Annotated[User_db, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[User_db, Depends(get_current_active_user)]
):
    return current_user
