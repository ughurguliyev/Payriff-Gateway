import json
import os

import requests

from .payment import Order, OrderStatus, RefundOrder
from .result_codes import ResultCodes


class PayriffGateway:
    BASE_URL = "https://api.payriff.com/api/v2/"

    SECRET_KEY = os.getenv("PAYRIFF_SECRET_KEY")

    def __init__(
            self,
            merchant_id: str,
            approve_url: str,
            cancel_url: str,
            decline_url: str) -> None:
        self.merchant_id = merchant_id
        self.approve_url = approve_url
        self.cancel_url = cancel_url
        self.decline_url = decline_url

        self.__order_instance = None
        self.__order_status_instance = None
        self.__refund_order_instance = None

    def __post(self, method_name: str, payload: dict) -> dict:
        url = f"{self.BASE_URL}{method_name}"
        headers = {
            "Content-Type": "application/json",
            "Authorization": self.SECRET_KEY,
            "Accept": "*",
            "Connection": "keep-alive",
        }
        r = requests.post(
            url,
            data=payload,
            headers=headers,
        )
        return r.json()

    def __build_json_payload(self, data: dict) -> dict:
        return json.dumps(data)

    def __build_order_object(self, initial_data: dict, result: dict) -> None:
        self.__order_instance = Order(
            amount=initial_data["body"]["amount"],
            currency=initial_data["body"]["currencyType"],
            status_code=result["code"],
            order_id=result["payload"]["orderId"],
            session_id=result["payload"]["sessionId"],
            payment_url=result["payload"]["paymentUrl"],
            transaction_id=result["payload"]["transactionId"],
        )

    def __build_order_status_object(self, initial_data: dict, result: dict) -> None:
        self.__order_status_instance = OrderStatus(
            order_id=initial_data["body"]["orderId"],
            status_code=result["code"],
            status=result["payload"]["orderStatus"],
            message=result["message"],
        )

    def __build_refund_order_object(self, result: dict) -> None:
        self.__refund_order_instance = RefundOrder(
            status_code=result["code"],
            internal_message=result["internalMessage"],
            message=result["message"],
        )

    def get_order(self) -> Order:
        return self.__order_instance

    def get_order_status_instance(self) -> OrderStatus:
        return self.__order_status_instance

    def create_order(
            self,
            amount: float,
            currency: str,
            direct_pay: bool = True,
            description: str = None,
            language: str = "AZ") -> dict:
        order_data = {
            "body": {
                "amount": amount,
                "approveURL": self.approve_url,
                "cancelURL": self.cancel_url,
                "currencyType": currency,
                "declineURL": self.decline_url,
                "description": description,
                "directPay": direct_pay,
                "language": language,
            },
            "merchant": self.merchant_id,
        }
        json_payload = self.__build_json_payload(data=order_data)
        result = self.__post(
            method_name="createOrder",
            payload=json_payload,
        )
        if result["code"] != ResultCodes.SUCCESS.value:
            raise Exception(result["message"])
        self.__build_order_object(initial_data=order_data, result=result)
        order = self.get_order()

        return {
            "status_code": order.status_code,
            "payment_url": order.payment_url,
            "session_id": order.session_id,
            "order_id": order.order_id
        }

    def get_order_status(
            self,
            order_id: str = None,
            language: str = "AZ",
            session_id: str = None) -> dict:
        order_data = {
            "body": {
                "language": language,
                "orderId": order_id,
                "sessionId": session_id,
            },
            "merchant": self.merchant_id,
        }
        json_payload = self.__build_json_payload(data=order_data)
        result = self.__post(
            method_name="getStatusOrder",
            payload=json_payload,
        )
        if result["code"] != ResultCodes.SUCCESS.value:
            raise Exception(result["message"])
        self.__build_order_status_object(initial_data=order_data, result=result)
        order_status = self.get_order_status_instance()

        return {
            "order_id": order_status.order_id,
            "status_code": order_status.status_code,
            "status": order_status.status,
            "message": order_status.message,
        }

    def refund_order(
            self,
            amount: float,
            order_id: str = None,
            session_id: str = None) -> dict:
        order_data = {
            "body": {
                "refundAmount": amount,
                "orderId": order_id,
                "sessionId": session_id,
            },
            "merchant": self.merchant_id,
        }
        json_payload = self.__build_json_payload(data=order_data)
        result = self.__post(
            method_name="refund",
            payload=json_payload,
        )
        self.__build_refund_order_object(result=result)
        refund_order = self.__refund_order_instance

        return {
            "status_code": refund_order.status_code,
            "internal_message": refund_order.internal_message,
            "message": refund_order.message,
        }
