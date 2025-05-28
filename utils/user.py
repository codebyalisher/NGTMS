from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException,status
from datetime import datetime, timedelta
from passlib.context import CryptContext
from config.settings import settings
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from models.user import User
from database import get_db 
import json
from models import *

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    if "sub" not in to_encode:
        raise ValueError("Missing 'sub' in token data")
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

def get_dropdown_options(db: Session) -> dict:    
    ticket_statuses = db.query(TicketStatus).all()
    ticket_sources = db.query(TicketSource).all()
    priorities = db.query(Priority).all()
    users = db.query(User).all()
    notification_types = db.query(NotificationType).all()
    sla_configurations = db.query(SlaConfiguration).all()
    contacts = db.query(Contact).all()
    purposes= db.query(Purpose).all()

    return {
        "ticket_statuses": [{"id": ts.id, "name": ts.name} for ts in ticket_statuses],
        "ticket_sources": [{"id": ts.id, "name": ts.name} for ts in ticket_sources],
        "priorities": [{"id": p.id, "name": p.name} for p in priorities],
        "users": [{"id": u.id, "name": u.name} for u in users],
        "notification_types": [{"id": nt.id, "name": nt.name} for nt in notification_types],
        "purposes": [{"id": p.id, "name": p.name} for p in purposes],
        "sla_configurations": [
            {
                "id": sla.id,
                "name": sla.name,
                "response_time": sla.response_time,
                "resolution_time": sla.resolution_time
            } for sla in sla_configurations
        ],
        "contacts": [{"id": c.id, "name": c.name} for c in contacts]
    }
