# coding:utf8
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User



class OrderData(models.Model):
    DISCIPLINE = (
        ('1', 'other'),
        ('2', 'physics')
    )

    TYPE_OF_WORK = (
        ('1', 'diplom'),
        ('2', 'referat')
    )
    created = models.DateTimeField(u'дана создания', default=datetime.now())

    discipline = models.CharField(u'учебная дисциплина', max_length=1, default='1', choices=DISCIPLINE)
    type = models.CharField(u'вид работы', max_length=1, default='1', choices=TYPE_OF_WORK)
    theme = models.TextField(u'тема работы', blank=True, null=True)
    content = models.TextField(u'содержание работы', blank=True, null=True)
    pages_num = models.IntegerField(u'примерное число страниц', blank=True, null=True)
    cost = models.FloatField(u'желаемая стоимость', blank=True, null=True)
    deadline = models.DateField(u'срок сдачи', blank=True, null=True)
    notes = models.TextField(u'примечания', blank=True, null=True)

    class Meta:
        verbose_name = u'Данные о заказе'
        verbose_name_plural = u'Данные о заказе'

    def __unicode__(self):
        return u'id: %s; theme: %s; content: %s;' % (self.id, self.theme, self.content)

class Order(models.Model):
    ORDER_STATUS = (
        ('1', u'in consideration'),
        ('2', u'waiting for payment'),
        ('3', u'payment confirmed'),
        ('4', u'done')
        )

    total = models.FloatField(u'цена', blank=True, null=True)
    #total_payed = models.FloatField(u'цена', blank=True, null=True)
    created = models.DateTimeField(default=datetime.now(), verbose_name=u'время создания заказа')
    order_data = models.OneToOneField(OrderData, blank=True, null=True, verbose_name=u'информация о заказе')
    status = models.CharField(u'статус', max_length=1, default='1', choices=ORDER_STATUS)
    user = models.ForeignKey(User, related_name='orders', blank=True, null=True)

    class Meta:
        verbose_name = u'Заказ'
        verbose_name_plural = u'Заказы'

    def __unicode__(self):
        if self.order_data:
            return "id: %s; theme: %s; content: %s" % ( self.id, self.order_data.theme, self.order_data.content)
        else:
            return self.created.strftime('%Y %m  %d')



class UserProfile(models.Model):

    user = models.ForeignKey(User, related_name='profiles')

    name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.IntegerField()

    def __unicode__(self):
        return self.user.email

