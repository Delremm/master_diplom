# coding:utf-8
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from django.utils.safestring import mark_safe

def datetime_ymd_tomedia(dest):
    return 'media/%s/%s/' % (dest, datetime.now().strftime('%Y%m%d'))


TYPE_OF_WORK = (
        ('1', u'другая работа'),
        ('2', u'реферат'),
        ('3', u'дипломный проект'),
	 ('4', u'курсовая работа'),
	 ('5', u'бизнес-план организации'),
	 ('6', u'экспериментальное исследование'),
	 ('7', u'аналитическая работа'),
	 ('8', u'дневник преддипл. практики'),
	 ('9', u'кандидатская диссертация'),
    )

class Order(models.Model):
    ORDER_STATUS = (
        ('1', u'в рассмотрении'),
        ('2', u'ожидание платежа'),
        ('3', u'платеж подтвержден'),
        ('4', u'работа выслана'),
        ('5', u'плохая работа'),
        ('6', u'не устраивает заказчика'),
        ('7', u'устраивает заказчика'),
        )

    total = models.FloatField(u'цена', blank=True, null=True)
    #total_payed = models.FloatField(u'цена', blank=True, null=True)
    created = models.DateTimeField(default=datetime.now(), verbose_name=u'время создания заказа')
    #delete later
    #order_data = models.OneToOneField(OrderData, blank=True, null=True, verbose_name=u'информация о заказе')
    status = models.CharField(u'статус', max_length=1, default='1', choices=ORDER_STATUS)
    user = models.ForeignKey(User, related_name='orders', blank=True, null=True)
    #delete later
    #work = models.OneToOneField(Work, blank=True, null=True, verbose_name=u'выполненная работа')

    class Meta:
        verbose_name = u'Заказ'
        verbose_name_plural = u'Заказы'

    def __unicode__(self):
        try:
            self.order_data
        except ObjectDoesNotExist:
            return "id: %s; created: %s" % (self.id, self.created.strftime('%Y %m  %d'))
        else:
            if self.order_data:
                return "id: %s; theme: %s; content: %s" % ( self.id, self.order_data.theme, self.order_data.content)
            else:
                return self.created.strftime('%Y %m  %d')



class OrderData(models.Model):
    DISCIPLINE = (
        ('1', u'другая дисциплина'),
        ('2', u'физика'),
	 ('2', u'математика'),
	 ('2', u'экономика'),
	 ('2', u'английский язык'),
	 ('2', u'биология'),
	 ('2', u'информатика'),
        )

    created = models.DateTimeField(u'дана создания', default=datetime.now())

    discipline = models.CharField(u'учебная дисциплина', max_length=1, default='1', choices=DISCIPLINE)
    type = models.CharField(u'вид работы', max_length=2, default='1', choices=TYPE_OF_WORK)
    theme = models.TextField(u'тема работы', blank=True, null=True)
    content = models.TextField(u'содержание работы', blank=True, null=True)
    pages_num = models.IntegerField(u'примерное число страниц', blank=True, null=True)
    cost = models.FloatField(u'желаемая стоимость в рублях', blank=True, null=True)
    deadline = models.DateField(u'срок сдачи', blank=True, null=True)
    notes = models.TextField(u'примечания', blank=True, null=True)

    order = models.OneToOneField(Order, null=True, blank=True, related_name='order_data', verbose_name=u'заказ')

    attached_file = models.FileField(u'файл с дополнениями',upload_to='media/order_data/%Y/%m/%d/', null=True, blank=True)

    class Meta:
        verbose_name = u'Данные о заказе'
        verbose_name_plural = u'Данные о заказе'

    def __unicode__(self):
        return u'id: %s; theme: %s; content: %s;' % (self.id, self.theme, self.content)

    def file_link(self):
        if self.attached_file:
            return mark_safe("<a href='%s'>скачать</a>" % (self.attached_file.url,))
        else:
            return "No attachment"
    file_link.short_description = u'скачать приложенный к заказу файл'
    file_link.allow_tags = True


class Work(models.Model):

    title = models.CharField(max_length=255, blank=True, null=True, verbose_name=u'название работы')
    content = models.TextField(blank=True, null=True, verbose_name=u'содержание')
    type = models.CharField(u'вид работы', blank=True, null=True, max_length=2, choices=TYPE_OF_WORK)

    work = models.FileField(upload_to=datetime_ymd_tomedia('works'))

    private = models.BooleanField(default=True)
    order = models.OneToOneField(Order, blank=True, null=True, related_name='work', verbose_name=u'заказ')

    class Meta:
        verbose_name = u'Выполненная работа'
        verbose_name_plural = u'Выполненные работы'

    def __unicode__(self):
        if self.title:
            return self.title
        else:
            return str(self.id)


class UserProfile(models.Model):

    user = models.ForeignKey(User, related_name='profiles')

    name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=12, blank=True, null=True)

    icq = models.CharField(u'icq', max_length=1000, blank=True, null=True)
    town = models.CharField(u'Город', max_length=1000, blank=True, null=True)
    institute = models.CharField(u'Учебное заведение', max_length=1000, blank=True, null=True)
    time_to_call = models.CharField(u'Удобное вребя для связи', max_length=1000, blank=True, null=True)

    def __unicode__(self):
        return self.user.email

