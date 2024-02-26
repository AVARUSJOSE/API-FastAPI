"""oAUTH2"""

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")


class Userroot(BaseModel):
    """clase que representa a usuarios root"""
    username: str
    fullname: str
    email: str
    disabled: bool


class UserDB(Userroot):
    """clase que representa a un usuario para base de datos"""
    password: str


users_root = {
    "avarusjose": {
        "username": "avarujose",
        "fullname": "Jose Izaguirre",
        "email": "joseaizaguirrep@gmail.com",
        "disabled": False,
        "password": "123456"
    },
    "avarusjose2": {
        "username": "avarujose2",
        "fullname": "Jose Perez",
        "email": "joseaizaguirrep2@gmail.com",
        "disabled": True,
        "password": "654321"
    }
}


def search_user_root(username: str):
    """funcion wue busca si usuario db concuerda con la base de datos creada como users_root"""
    if username in users_root:
        return UserDB(**users_root[username])


def search_user_db(username: str):
    """funcion wue busca si usuario db concuerda con la base de datos creada como users_root"""
    if username in users_root:
        return Userroot(**users_root[username])


async def current_user(token: str = Depends(oauth2)):
    """funcion que autentica el usuario luego de enviar datos de autenticacion"""
    user_current = search_user_db(token)
    if not user_current:
        raise HTTPException(status_code=401,
                            detail="Credenciales de autenticacion invalidas",
                            headers={"www-Authenticate": "bearer"})
    if user_current.disabled:
        raise HTTPException(status_code=400, detail="Usuario inactivo")
    return user_current


@app.post("/login/")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    """busqueda de usuario a auntenticar"""
    user_root = users_root.get(form.username)
    if not user_root:
        raise HTTPException(
            status_code=400, detail="El usuario no es el correcto")
    user = search_user_root(form.username)
    if not form.password == user.password:
        raise HTTPException(
            status_code=400, detail="La contraseña es incorrecta")

    return {"acces_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def me(user: Userroot = Depends(current_user)):
    """funcion con criterio de dependencia criterio de dependencia, retorna el usuario"""
    return user
