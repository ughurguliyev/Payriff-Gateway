import unittest

from payriff_gateway.base import PayriffGateway


class PayriffGatewayTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.gateway = PayriffGateway(
            merchant_id='your_merchant_id',
            approve_url='https://example.com/approve',
            cancel_url='https://example.com/cancel',
            decline_url='https://example.com/decline',
        )
        self.order = self.gateway.create_order(
            amount=100,
            currency='AZN',
            direct_pay=True,
            description='Test order',
            language='AZ',
        )
    
    def test_create_order(self) -> None:
        self.assertEqual(self.order['status_code'], '00000')
    
    def test_get_order_status(self) -> None:
        result = self.gateway.get_order_status(
            order_id=self.order['order_id'],
            language='AZ',
            session_id=self.order['session_id'],
        )
        self.assertEqual(result['status_code'], '00000')
    
    def test_refund_order(self) -> None:
        result = self.gateway.refund_order(
            amount=100,
            order_id=self.order['order_id'],
            session_id=self.order['session_id'],
        )
        self.assertEqual(result['status_code'], '01000')