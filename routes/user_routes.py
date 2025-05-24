from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from schemas.user import LoginRequest, UserLoginResponse
from utils.user import verify_password, create_access_token
from models.user import User

router = APIRouter(prefix="/user", tags=["user"])

@router.post("/login", response_model=dict)
def login_user(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    token = create_access_token({"sub": user.email})

    return {
        "message": "Login successful",
        "status_code": status.HTTP_200_OK,
        "data": {
            "token": token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "picture": user.picture,
            }
        #     "role": {
        #         "id": user.role.id if user.role else None,
        #         "name": user.role.name if user.role else None,
        #         "status": user.role.status if user.role else None,
        #     },
        #     "department": {
        #         "id": user.department.id if user.department else None,
        #         "name": user.department.name if user.department else None,
        #         "status": user.department.status if user.department else None,
        #     },
        
    }
    }