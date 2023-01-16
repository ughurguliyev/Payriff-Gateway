from dataclasses import dataclass


@dataclass
class Order:
    amount: float
    currency: str
    status_code: str
    order_id: str
    session_id: str
    payment_url: str
    transaction_id: str


@dataclass
class OrderStatus:
    order_id: str
    status_code: str
    status: str
    message: str


@dataclass
class RefundOrder:
    status_code: str
    internal_message: str
    message: str