from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="admin/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")