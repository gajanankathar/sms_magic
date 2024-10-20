import logging

from fastapi import APIRouter, Body, HTTPException, Path, Query, status
from typing import List, Optional

from .database import DB
from .utils import get_next_sequence_id
from .schemas import Order, Product, User, OrderResponse, ProductResponse, UserResponse

# Configure logging
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)

# Create console handler and set level to info
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# Create formatter
formatter = logging.Formatter('%(levelname)s:    %(message)s')

# Add formatter to ch
ch.setFormatter(formatter)

# Add ch to logger
_logger.addHandler(ch)


# ================================== Validation ================================================
async def validate_user(user_id: int):
    """
    Method to validate given user id exist or not in DB.

    Arguments:
        user_id (int): Id of the user

    Returns:
         It returns user details for the given user id if exists other returns bad request response.
    """
    users = list(filter(lambda user: user["id"] == user_id, DB["users"]))
    if not users:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user!")
    return users[0]


async def validate_product(product_id):
    """
    Method to validate given product id exist or not in DB.

    Arguments:
        product_id (int): Id of the product

    Returns:
         It returns product details for the given product id if exists other returns bad request response.
    """
    products = list(filter(lambda product: product["id"] == product_id, DB["products"]))
    if not products:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid product {product_id}!")
    return products[0]

# =================================== User Routes ============================================= #

user_route = APIRouter(
    prefix="/v1",
    responses={404: {"description": "Not found"}},
)


@user_route.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def add_user(user_details: User = Body(...)):
    """
    Add user route to add user details into user table.
    """
    user_details = user_details.dict()
    next_id = await get_next_sequence_id("users")
    user_details["id"] = next_id
    DB["users"].append(user_details)
    return user_details


@user_route.get("/users")
async def get_all_users():
    """
    Get all users route to returns all users from DB.
    """
    return DB["users"]


@user_route.get("/users/{user_id}")
async def get_user(user_id: int = Path(..., title="Id of the user")):
    """
    Get user route to returns user for the given user ID.
    """
    users = list(filter(lambda user: user["id"] == user_id, DB["users"]))
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")
    return users[0]


# =================================== Product Routes ============================================= #

product_route = APIRouter(
    prefix="/v1",
    responses={404: {"description": "Not found"}},
)


@product_route.post("/products", status_code=status.HTTP_201_CREATED, response_model=ProductResponse)
async def add_product(product_details: Product = Body(...)):
    """
    Add product route to add product details into product table.
    """
    product_details = product_details.dict()
    next_id = await get_next_sequence_id("products")
    product_details["id"] = next_id
    DB["products"].append(product_details)
    return product_details


@product_route.get("/products", response_model=List[ProductResponse])
async def get_all_product():
    """
    API to retrieve all products.
    """
    return DB["products"]


async def add_product_to_browse_history(user_id: int, product_id: int):
    """
    Method to record product in product browse history against given user.

    Arguments:
        user_id (int): ID of the user
        product_id (int): ID of the product
    """
    _tbl_browse_history = DB["browse_history"]
    try:
        _tbl_browse_history[user_id].add(product_id)
        _logger.debug(f"Product {product_id} is added in the product browsing history of user {user_id}.")
    except KeyError:
        users = list(filter(lambda user: user["id"] == user_id, DB["users"]))
        # If user exists in the user table then create it's product browsing history.
        if users:
            _logger.info(f"This user ({user_id}), first time browsing product on the portal!")
            _tbl_browse_history[user_id] = {product_id}
            _logger.debug(f"Product {product_id} is added in the product browsing history of user {user_id} .")


@product_route.get("/products/recommendation/users/{user_id}")
async def get_recommendation(user_id: int = Path(..., title="Id of the user [session]")):
    """
    API to retrieve recommended products for given user.
    """
    _tbl_browse_history = DB["browse_history"]
    _tbl_purchase_history = DB["purchase_history"]
    _tbl_products = DB["products"]

    await validate_user(user_id)
    browse_product_ids = _tbl_browse_history.get(user_id, set())
    purchase_product_ids = _tbl_purchase_history.get(user_id, set())
    product_to_recommend = browse_product_ids.union(purchase_product_ids)
    products = list(filter(lambda product: product.get("id") in product_to_recommend, _tbl_products))
    return {"products": products}


@product_route.get("/products/{prod_id}/users/{user_id}", response_model=ProductResponse)
async def get_product(
    prod_id: int = Path(..., title="Id of the product"),
    user_id: int = Path(..., title="Id of the user [session]")
):
    """
    API to retrieve product by it's ID.
    """
    products = list(filter(lambda product: product["id"] == prod_id, DB["products"]))
    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found!")
    # add product to user product browsing history
    await add_product_to_browse_history(user_id, prod_id)
    return products[0]

# =================================== Order Routes ============================================= #

order_route = APIRouter(
    prefix="/v1",
    responses={404: {"description": "Not found"}},
)


@order_route.get("/orders", response_model=List[OrderResponse])
async def get_all_orders():
    """
    API to get all list of products
    """
    return DB["orders"]


@order_route.get("/orders/{order_id}", response_model=OrderResponse)
async def get_order(order_id: int = Path(..., title="ID of the order")):
    """
    API to get order by it's ID.
    """
    _orders = DB["orders"]
    orders = list(filter(lambda order: order["id"] == order_id, _orders))
    if not orders:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found!")
    return orders[0]


@order_route.get("/orders/users/{user_id}", response_model=List[OrderResponse])
async def get_orders_by_user(user_id: int = Path(..., title="Orders by it's user")):
    """
    API to get all orders of the given user
    """
    _orders = DB["orders"]
    orders = list(filter(lambda order: order["customer_id"] == user_id, _orders))
    if not orders:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order not found for user {user_id}")
    return orders


async def add_product_to_purchase_history(user_id: int, product_id: int):
    """
    Method to record product in product purchase history against given user.

    Arguments:
        user_id (int): ID of the user
        product_id (int): ID of the product
    """
    _tbl_purchase_history = DB["purchase_history"]
    try:
        _tbl_purchase_history[user_id].add(product_id)
        _logger.debug(f"Product {product_id} is added in the product browsing history of user {user_id}.")
    except KeyError:
        users = list(filter(lambda user: user["id"] == user_id, DB["users"]))
        # If user exists in the user table then create it's product browsing history.
        if users:
            _logger.info(f"This user ({user_id}), first time browsing product on the portal!")
            _tbl_purchase_history[user_id] = {product_id}
            _logger.debug(f"Product {product_id} is added in the product browsing history of user {user_id} .")


@order_route.post("/orders", response_model=OrderResponse)
async def add_order(order_details: Order = Body(..., title="Order details")):
    """
    API to create order with given order details.
    """
    _orders = DB["orders"]
    order_details = order_details.dict()
    # validate customer and products
    user = await validate_user(order_details.get("customer_id"))
    products = []
    for orderline in order_details.get("orderlines", []):
        products.append(await validate_product(orderline.get("product_id")))
    # get next order sequence id
    next_id = await get_next_sequence_id("orders")
    order_details["id"] = next_id
    # add product to the purchase history
    for product in products:
        await add_product_to_purchase_history(user.get("id"), product.get("id"))
    # create order with order details
    _orders.append(order_details)
    return order_details
