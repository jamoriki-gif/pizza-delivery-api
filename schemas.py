from pydantic import BaseModel
from typing import Optional




class SignUPModel(BaseModel):
    id: Optional[int] 
    username: str
    email: str
    password: str
    is_staff: Optional[bool] 
    is_active: Optional[bool] 


    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "username": "johndoe",
                "email": "johndoe@gmail.com",
                "password": "password123",
                "is_staff": False,
                "is_active": True
            }
        }



class settings(BaseModel):
        authjwt_secret_key: str="881b3af4b651ebd0e7e2bbc98351797ac21fd476d8c348cebd05b604dff51fa3"



class LoginModel(BaseModel):
    username: str
    password: str

  


class OrderModel(BaseModel):
    id: Optional[int]
    user_id: Optional[int]
    pizza_name: str
    quantity: int
    price: float
    pizza_size: Optional[str] = "medium"
    order_status: Optional[str] = "pending"

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "user_id": 1,
                "pizza_name": "Margherita",
                "quantity": 2,
                "price": 15.99
            }
        }

    class order_status_model(BaseModel):
        order_status: Optional[str] = "pending"
        class Config:
            schema_extra = {
                "example": {
                    "order_status": "pending"
                }
            }
       


