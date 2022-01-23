from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, status,APIRouter, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel



router = APIRouter()
oauth_scheme = OAuth2PasswordBearer(tokenUrl='token')

@router.post("/token")
async def token_generate(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    }
    print(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    # user = UserInDB(**user_dict)
    print(form_data.password)
    # hashed_password = fake_hash_password(form_data.password)
    # if not hashed_password == user.hashed_password:
    #     raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user_dict['username'], "token_type": "bearer"}

@router.get("/gift")
async def get_gift(token: str = Depends(oauth_scheme)):
    print(token)
    return {"gift":"HEY"}
