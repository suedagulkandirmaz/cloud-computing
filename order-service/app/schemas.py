from pydantic import BaseModel

class OrderCreate(BaseModel):
    customer_name: str
    product_id: int
    quantity: int


class LoginRequest(BaseModel):
    username: str
    password: str

class OrderUpdate(BaseModel):
    customer_name: str
    product_id: int
    quantity: int