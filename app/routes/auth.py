from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import schemas, utils
from ..core import oauth2
from ..db import models, session
from ..db.repository.auth import verify_user_isactive, verify_credential

router = APIRouter(tags=['Authentication'])


@router.post('/login', response_model=schemas.Token)
def login_for_access_token(user_credentials: OAuth2PasswordRequestForm = Depends(),
                           db: Session = Depends(session.get_db)):

    user = verify_credential(email=user_credentials.username, password=user_credentials.password, db=db)

    # user not found or invalid password
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Invalid credentials")

    # ensure the user is active
    user = verify_user_isactive(user)

    # user account is delete == deactivated
    if not user:
        raise HTTPException(status_code=status.HTTP_423_LOCKED,
                            detail=f"User account has been deactivated. Please contact system administrators")

    # create a token
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
