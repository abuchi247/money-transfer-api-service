from fastapi import status, HTTPException, Depends, APIRouter, Response
from sqlalchemy.orm import Session
from app.db.session import get_db
from .. import schemas
from ..core import oauth2
from ..db import models
from ..db.repository.user import UserRepository
from typing import List, Optional

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # check if user already exists in the database
    user_found = UserRepository.retrieve_user_by_email(email=user.email, db=db)

    # user email already taken
    if user_found:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"User with email: {user.email!r} already taken")

    # create a new user
    new_user = UserRepository.create_new_user(user=user, db=db)

    return new_user


@router.get("/", response_model=List[schemas.ShowUser])
def get_users(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # user must be an admin to view all other users
    if not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")

    results = UserRepository.list_users(db=db, limit=limit, search_email_phrase=search, skip=skip)

    return results


@router.get("/{id}", response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    # user must be an admin to view all other users or current user can see his own information
    if not current_user.is_superuser and current_user.id != id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")

    user = UserRepository.retrieve_user_by_id(id=id, db=db)
    # user not found
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id!r} not found")
    return user


@router.put("/{id}", response_model=schemas.ShowUser)
def update_user(id: int, user: schemas.UserUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(
    oauth2.get_current_user)):
    # user must be an admin to view all other users or user isn't changing his own information
    if not current_user.is_superuser and current_user.id != id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")

    # check if user exists
    user_found = UserRepository.retrieve_user_by_id(id=id, db=db)

    # user not found
    if not user_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id!r} not found")

    # check if user email already taken by another user
    user_with_email_already_exists = UserRepository.retrieve_user_by_email(email=user.email, db=db)


    # user email exists but not ownered by the user we want to update
    if user_with_email_already_exists and user_with_email_already_exists.id != id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"User with email: {user.email!r} already taken")

    user_updated = UserRepository.update_user_by_id(id=id, user=user.dict(), db=db)
    # # we should never get here unless user was updater by another user at the same time.
    # if not user_updated:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"User no longer exists. Something went wrong")

    return user_updated


@router.delete('/{id}')
def delete_user(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    # can only be performed by an admin
    if not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")

    # # logged in user cannot delete their information
    # if current_user.id == id:
    #     raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
    #                         detail=f"Logged in users are prohibited from deleting their information")

    user_deactivated = UserRepository.deactivate_user_by_id(id=id, db=db)

    # user not found
    if not user_deactivated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id!r} not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)