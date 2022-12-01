from clickuz.views import ClickUzMerchantAPIView
from clickuz import ClickUz

class OrderCheckAndPayment(ClickUz):
    def check_order(self, order_id: str, amount: str):
        print(order_id, amount)
        return self.ORDER_FOUND

    def successfully_payment(self, order_id: str, transaction: object):
        print(order_id)


class ClickView(ClickUzMerchantAPIView):
    VALIDATE_CLASS = OrderCheckAndPayment