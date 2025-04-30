from settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

# secret em bcrypt - $2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW
# bolinhas em bcrypt - $2b$12$5lY1RPNbyFHP2bK/JjjY0eyiIJnmxUfUE0OHi81xg2nN1w1NoKznK
db_clientes_api = {
    "abc": {
    "username": "abc",
    "full_name": "Abc dos Testes",
    "email": "abc@example.com",
    "password": "$2b$12$5lY1RPNbyFHP2bK/JjjY0eyiIJnmxUfUE0OHi81xg2nN1w1NoKznK",
    "disabled": False,
    },
    "bolinhas": {
    "username": "bolinhas",
    "full_name": "Bolinhas dos Testes",
    "email": "bolinhas@example.com",
    "password": "$2b$12$5lY1RPNbyFHP2bK/JjjY0eyiIJnmxUfUE0OHi81xg2nN1w1NoKznK",
    "disabled": True,
    },
    }

class Token(BaseModel):
    access_token: str  
    token_type: str
    expire_minutes: int

class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None  
    disabled: bool | None = None   

class UserInDB(User):
    password: str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # cifra da senha do usuário
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") # token

def verify_password(plain_password, password):
    return pwd_context.verify(plain_password, password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
     return False
    if not verify_password(password, user.password):
     return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials",
headers={"WWW-Authenticate": "Bearer"},)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db_clientes_api, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)],):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

### rota para autenticacao e geracao de token
from fastapi import APIRouter
router = APIRouter()

@router.post('/token', tags=["Token JWT"])
async def login_for_access_token(from_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = authenticate_user(db_clientes_api, from_data.username, from_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"},)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return Token(access_token=access_token, token_type="bearer", expire_minutes=ACCESS_TOKEN_EXPIRE_MINUTES)


@router.get("/token/logado",response_model=User,tags=["Token JWT"])
async def red_users_me(current_user:Annotated[User,Depends(get_current_active_user)],):
    return current_user
    
