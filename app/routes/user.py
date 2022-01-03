from fastapi import status, HTTPException, Depends, APIRouter
from starlette.status import HTTP_201_CREATED
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, utils, oauth2

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.post("/", status_code=HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user_found = db.query(models.User).filter(models.User.email == user.email).first()

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


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id!r} not found")
    return user
