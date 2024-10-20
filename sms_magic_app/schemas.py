from pydantic import BaseModel
from typing import Any, Dict, List


class User(BaseModel):
    name: str


class UserResponse(User):
    id: int


class Product(BaseModel):
    name: str


class ProductResponse(Product):
    id: int


class Orderline(BaseModel):
    product_id: int
    qty: int


class Order(BaseModel):
    customer_id: int
    orderlines: List[Orderline]


class OrderResponse(Order):
    id: int




