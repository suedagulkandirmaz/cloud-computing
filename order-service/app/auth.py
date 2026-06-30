from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# =====================
# CONFIG
# =====================
SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

security = HTTPBearer()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# =====================
# FAKE USER DB (FIXED)
# =====================
fake_user = {
    "username": "admin",
    "password": pwd_context.hash("admin123")  # sadece 1 kere (startup için OK)
}

# =====================
# PASSWORD FUNCTIONS
# =====================
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# =====================
# AUTH USER
# =====================
def authenticate_user(username: str, password: str):
    if username != fake_user["username"]:
        return False

    return verify_password(password, fake_user["password"])

# =====================
# JWT TOKEN
# =====================
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({
        "exp": expire,
        "sub": data.get("sub")  # FIX: subject eklenmiş olmalı
    })

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# =====================
# CURRENT USER
# =====================
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

        return username

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )