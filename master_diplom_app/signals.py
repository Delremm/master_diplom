from models import Order, OrderData

from robokassa.signals import result_received

def payment_received(sender, **kwargs):
    order = Order.objects.get(id=kwargs['InvId'])
    print order.staus
    order.status = '3'
    #order.paid_sum = kwargs['OutSum']
    #order.extra_param = kwargs['extra']['my_param']
    order.save()
    print order.status

result_received.connect(payment_received)
