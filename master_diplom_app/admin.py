# coding:utf8

from django.contrib import admin
from django.template.defaultfilters import escape
from django.core.urlresolvers import reverse
from django.forms.widgets import Widget
from django.db import models


from django.utils.safestring import mark_safe


from models import Order, OrderData, UserProfile, Work

from email_utils import send_payment_notification


def add_link_field(target_model = None, field = '', app='', field_name='link',
                   link_text=unicode):
    def add_link(cls):
        reverse_name = target_model or cls.model.__name__.lower()
        def link(self, instance):
            app_name = app or instance._meta.app_label
            reverse_path = "admin:%s_%s_change" % (app_name, reverse_name)
            link_obj = getattr(instance, field, None) or instance
            url = reverse(reverse_path, args = (link_obj.id,))
            return mark_safe("<a href='%s'>%s</a>" % (url, link_text(link_obj)))
        link.allow_tags = True
        link.short_description = reverse_name + ' link'
        setattr(cls, field_name, link)
        cls.readonly_fields = list(getattr(cls, 'readonly_fields', [])) +\
                              [field_name]
        return cls
    return add_link

@add_link_field('orderdata','order_data', 'master_diplom_app')
class OrderAdmin(admin.ModelAdmin):
    actions = ['payment_notification']

    def payment_notification(self, request, queryset):
        #update status to "waiting for payment"
        for q in queryset:
            if q.total:
                try:
                    send_payment_notification(request, q.user, order=q)
                except:
                    message_bit = u'произошла ошибка, при отправке письма с уведомлением об оплате'
                else:
                    q.status = '2'
                    message_bit = u'письмо с уведомлением об оплате отправлено'
                    q.save()
            else:
                message_bit = u'цена не назначена'
        self.message_user(request, message_bit)
    payment_notification.short_description = u"Уведомить об оплате"

    def send_work(self, request, queryset):
        for q in queryset:
            if q.work_file:
                pass
            else:
                message_bit = u'работа не загружена'
        self.message_user(request, queryset)
    send_work.short_description = u'Выслать работу'





admin.site.register(Order, OrderAdmin)
admin.site.register(OrderData)
admin.site.register(Work)