from fastapi import status, HTTPException, Depends, APIRouter, Response
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from .. import schemas, models, utils, oauth2
from typing import List, Optional

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # check if user already exists in the database
    user_found = db.query(models.User).filter(models.User.email == user.email).first()

    # user email already taken
    if user_found:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"User with email: {user.email!r} already taken")

    # hash the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    # create a new user
    new_user = models.User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # retrieve the new user we created and store that in the new_user variable
    return new_user


@router.get("/", response_model=List[schemas.UserOut])
def get_users(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # user must be an admin to view all other users
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")

    results = db.query(models.User).filter(models.User.id != current_user.id).filter(models.User.email.contains(search)).limit(limit).offset(skip).all()
    print(results)
    return results


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    # user must be an admin to view all other users or current user can see his own information
    if current_user.role != "admin" and current_user.id != id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")

    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id!r} not found")
    return user


@router.put("/{id}", response_model=schemas.UserOut)
def update_user(id: int, user: schemas.UserBase, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    # user must be an admin to view all other users or user isn't changing his own information
    if current_user.role != "admin" and current_user.id != id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")
    # user query
    user_query = db.query(models.User).filter(models.User.id == id)

    # user not found
    if not user_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id!r} not found")

    # check if the new email already exists in the database
    user_with_new_email_exists = db.query(models.User).filter(models.User.email == user.email).first()

    # new email already taken
    if user_with_new_email_exists.id != id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"User with email: {user.email!r} already taken")

    # update user with new information
    user_query.update(user.dict(), synchronize_session=False)
    db.commit()

    return user_query.first()


@router.delete('/{id}')
def delete_user(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    # can only be performed by an admin
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")

    # logged in user cannot delete their information
    if current_user.id == id:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail=f"Logged in users are prohibited from deleting their information")

    user_query = db.query(models.User).filter(models.User.id == id)

    # user not found
    if not user_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id!r} not found")

    # delete user from db
    user_query.delete(synchronize_session=False)

    # commit changes
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)