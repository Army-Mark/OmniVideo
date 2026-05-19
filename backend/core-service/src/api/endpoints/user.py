from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Depends
from jose import JWTError, jwt
from passlib.context import CryptContext
from models.schemas import UserCreate, UserLogin, UserResponse, TokenResponse
from models.database import settings

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

fake_users_db = {}


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


@router.post("/register")
async def register(user_data: UserCreate):
    """用户注册"""
    if user_data.username in fake_users_db:
        raise HTTPException(status_code=400, detail="用户名已存在")

    user_id = len(fake_users_db) + 1
    hashed_password = get_password_hash(user_data.password)

    fake_users_db[user_data.username] = {
        "id": user_id,
        "username": user_data.username,
        "email": user_data.email,
        "password_hash": hashed_password,
        "created_at": datetime.now(),
    }

    return {
        "code": 200,
        "message": "注册成功",
        "data": UserResponse(
            id=user_id,
            username=user_data.username,
            email=user_data.email,
            created_at=fake_users_db[user_data.username]["created_at"],
        ),
    }


@router.post("/login")
async def login(user_data: UserLogin):
    """用户登录"""
    user = fake_users_db.get(user_data.username)
    if not user or not verify_password(user_data.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="用户名或密码错误")

    access_token = create_access_token(data={"sub": user["username"]})

    return {
        "code": 200,
        "message": "登录成功",
        "data": TokenResponse(
            access_token=access_token,
            user=UserResponse(
                id=user["id"],
                username=user["username"],
                email=user["email"],
                created_at=user["created_at"],
            ),
        ),
    }


@router.get("/profile")
async def get_profile():
    """获取用户信息"""
    return {
        "code": 200,
        "data": UserResponse(
            id=1,
            username="demo",
            email="demo@example.com",
            created_at=datetime.now(),
        ),
    }
