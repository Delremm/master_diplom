# coding:utf-8

from models import Order, OrderData

from robokassa.signals import result_received
from master_diplom_app.email_utils import send_payment_success_email



def payment_received(sender, **kwargs):
    order = Order.objects.get(id=kwargs['InvId'])
    order.status = '3'
    #order.paid_sum = kwargs['OutSum']
    #order.extra_param = kwargs['extra']['my_param']
    send_payment_success_email(order.user, order=order)
    order.save()

result_received.connect(payment_received)
