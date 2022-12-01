from paycomuz.views import MerchantAPIView
from paycomuz import Paycom
from orders.models import Order


class CheckOrder(Paycom):
    def check_order(self, amount, account, *args, **kwargs):
        print(amount, account)
        order_id = account.get("order_id", None)
        order = Order.objects.filter(id=order_id)
        if order.exists():
            order = order.first()
            print(order.total_price)
            print(amount / 100)
            if float(order.total_price) == (amount / 100):
                return self.ORDER_FOUND
            else:
                return self.INVALID_AMOUNT
        
        return self.ORDER_NOT_FOND
        
    def successfully_payment(self, account, transaction, *args, **kwargs):
        order_id = account.get("order_id", None)
        if order_id:
            order = Order.objects.filter(id=order_id)
            if order.exists():
                order = order.first()
                order.status = 'Completed'
                order.save()
            else:
                return False
        else:
            return False
        
        return True


    def cancel_payment(self, account, transaction, *args, **kwargs):
        order_id = account.get("order_id", None)
        if order_id:
            order = Order.objects.filter(id=order_id)
            if order.exists():
                order = order.first()
                order.status = 'Cancelled'
                order.save()
            else:
                return False
        else:
            return False
        
        return True
        

class PaymeView(MerchantAPIView):
    VALIDATE_CLASS = CheckOrder