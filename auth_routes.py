from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from database import Session,engine
from models import User
from schemas import SignUPModel,loginModel
from fastapi import Depends
from fastapi import HTTPException, status
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder


auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


session=Session(bind=engine)


@auth_router.get("/")
async def hello():
    return {"message": "Hello, Auth!"}




@auth_router.post("/signup",  status_code=status.HTTP_201_CREATED)
async def register_user(user: SignUPModel):

    # Check if the user already exists
    db_email = session.query(User).filter(User.email == user.email).first()
    if db_email :
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"

        )
    


    db_username = session.query(User).filter(User.username == user.username).first()
    if db_username :
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )

    # Create
    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_staff=user.is_staff,
        is_active=user.is_active
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user






@app.get("/")
async def root():
    return {"message": "Hello, World!"}





#login route


@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def login(user: loginModel, Authorize: AuthJWT = Depends()):
        db_user = session.query(User).filter(User.username == user.username).first()
        if not db_user or not check_password_hash(db_user.password, user.password):
            raise HTTPException(status_code=400, detail="Invalid username or password")

        access_token = Authorize.create_access_token(subject=db_user.username)
        refresh_token = Authorize.create_refresh_token(subject=db_user.username)
        
        response = {"access_token": access_token, "refresh_token": refresh_token}

        return jsonable_encoder(response) 








