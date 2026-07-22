from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi import status
from fastapi_jwt_auth import AuthJWT
from models import Order, User
from database import Session, engine
from schemas import OrderModel
from fastapi.encoders import jsonable_encoder



order_router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)


Session = Session(bind=engine)

@order_router.get("/")
async def hello(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return {"message": "Hello, Order!"}



@order_router.post("/orders", status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderModel, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Unauthorized")

    current_user = Authorize.get_jwt_subject()

    user=Session(bind=engine).query(User).filter(User.id == current_user).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_order = Order(
        user_id=current_user,
        pizza_name=order.pizza_name,
        quantity=order.quantity,
        price=order.price,
        pizza_size=order.pizza_size,
        order_status=order.order_status
    )

    new_order.user=user

    session=Session(bind=engine)
    session.add(new_order)
    session.commit()

    response = {
        
            "message": "Order created successfully",
            "order": jsonable_encoder(new_order),
            "id": new_order.id,
            "order_status": new_order.order_status,
        }
    

    return jsonable_encoder(response)




@order_router.get("/orders/{order_id}", status_code=status.HTTP_200_OK)
async def list_all_orders(order_id: int, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Unauthorized")

    current_user = Authorize.get_jwt_subject()

    user = Session.query(User).filter(User.id == current_user).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user = Session.query(Order).filter(Order.id == order_id, Order.user_id == current_user).first()
    if user.is_staff:
        order=Session.query(Order).all()
       
        return jsonable_encoder(order)

    raise HTTPException(status_code=403, detail="You are not authorized to view all orders")
   

@order_router.get("/orders/{order_id}", status_code=status.HTTP_200_OK)
async def get_order(order_id: int, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Unauthorized")

    current_user = Authorize.get_jwt_subject()

    user = Session.query(User).filter(User.id == current_user).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    order = Session.query(Order).filter(Order.id == order_id, Order.user_id == current_user).first()
    if current_user.is_staff:
        order=Session.query(Order).filter(Order.id == order_id).first()
        return jsonable_encoder(order)
    raise HTTPException(status_code=403, detail="You are not authorized to view this order")
    
