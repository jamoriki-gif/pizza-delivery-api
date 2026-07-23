from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi import status
from fastapi_jwt_auth import AuthJWT
from models import Order, User
from database import Session, engine
from schemas import OrderModel,order_status_model
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




@order_router.get("/user/orders", status_code=status.HTTP_200_OK)
async def get_user_order( Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Unauthorized")

    current_user = Authorize.get_jwt_subject()

    user = Session.query(User).filter(User.id == current_user).first()
    if not user:
        raise HTTPException(status_code=401, detail="invalid token")

    user=Authorize.get_jwt_subject()
    current_user=Session.query(User).filter(User.user_name == user).first()
    return jsonable_encoder(current_user.orders)




@order_router.get("/user/orders/{order_id}", status_code=status.HTTP_200_OK)
async def get_specific_order(order_id: int, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Unauthorized")

    subject= Authorize.get_jwt_subject()
    current_user=Session.query(User).filter(User.username == subject).first()

    order= current_user.orders


    for o in order:
        if o.id == id:
            return jsonable_encoder(o)

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="No order found for the current user with the provided order ID.")
    


@order_router.put("/user/orders/{order_id}", status_code=status.HTTP_200_OK)
async def update_order(order_id: int, order_update: OrderModel, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Unauthorized")

    subject= Authorize.get_jwt_subject()
    order_to_update=Session.query(Order).filter(Order.id == order_id).first()


    order_to_update.quantity=order_id.quantity
    order_to_update.pizza_size=order_id.pizza_size
    Session.commit()

    return jsonable_encoder(order_to_update)



@order_router.patch("/user/orders/{order_id}", status_code=status.HTTP_200_OK)
async def update_order_status(order_id: int, order_status_update: order_status_model, Authorize: AuthJWT = Depends()):
    
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Unauthorized")

    username= Authorize.get_jwt_subject()
    current_user=Session.query(User).filter(User.username == username).first()
    if current_user.is_staff==False:
        raise HTTPException(status_code=403, detail="You are not authorized to update order status")

    order_to_update=Session.query(Order).filter(Order.id == order_id).first()

    order_to_update.order_status=order_status_update.order_status

    response={
        "id": order_to_update.id,
        "user_id": order_to_update.user_id,
        "quantity": order_to_update.quantity,
        "pizza_size": order_to_update.pizza_size,
        "order_status": order_to_update.order_status
    }
    Session.commit()
    return jsonable_encoder(response)



@order_router.delete("/user/orders/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(order_id: int, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Unauthorized")

    username= Authorize.get_jwt_subject()
    current_user=Session.query(User).filter(User.username == username).first()
    if current_user.is_staff==False:
        raise HTTPException(status_code=403, detail="You are not authorized to delete orders")

    order_to_delete=Session.query(Order).filter(Order.id == order_id).first()

    if not order_to_delete:
        raise HTTPException(status_code=404, detail="Order not found")

    Session.delete(order_to_delete)
    Session.commit()

    return order_to_delete

