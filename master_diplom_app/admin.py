# coding:utf-8

from django.contrib import admin
from django.core.urlresolvers import reverse



from django.utils.safestring import mark_safe


from models import Order, OrderData, UserProfile, Work

from email_utils import send_payment_notification, send_work


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

class OrderWorkInline(admin.TabularInline):
    model = Work
    extra = 0

class OrderDataInline(admin.StackedInline):
    model = OrderData
    extra = 0
    #fields = ('discipline', 'type', 'theme', 'content', 'pages_num', 'cost', 'deadline', 'notes', 'created', 'order', 'file_link')
    readonly_fields = ('file_link',)

@add_link_field('orderdata','order_data', 'master_diplom_app')
class OrderAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    fieldsets = (
        (None, {
            'fields': ('status', 'total',),
            }),
        (u'Дополнительно', {
            'classes': ('collapse',),
            'fields': ('created', 'user'),
        }),
    )
    inlines = [OrderDataInline, OrderWorkInline]

    list_display = ('id', 'order_data_theme', 'status', 'created', 'user_email')

    def order_data_theme(self, obj):
        return ("%s" % obj.order_data.theme)
    order_data_theme.short_description = u'тема работы'

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'email'

    list_filter = ('status',)
    raw_id_fields = ('user',)
    search_fields = (['order_data__theme', 'order_data__content'])
    readonly_fields = ('status',)
    actions = ['payment_notification', 'send_work']

    def payment_notification(self, request, queryset):
        #update status to "waiting for payment"
        for q in queryset:
            if q.total:
                try:
                    send_payment_notification(request, q.user, order=q)
                except:
                    message_bit = u'произошла ошибка, при отправке письма с уведомлением об оплате (заказ id: %s)' % q.id
                else:
                    q.status = '2'
                    message_bit = u'письмо с уведомлением об оплате отправлено (заказ id: %s)' % q.id
                    q.save()
            else:
                message_bit = u'цена не назначена (заказ id: %s)' % q.id
        self.message_user(request, message_bit)
    payment_notification.short_description = u"Уведомить об оплате"

    def send_work(self, request, queryset):
        for q in queryset:
            if q.work and ((q.status == '3') or (q.status == '4')):
                try:
                    send_work(request, request.user, order=q)
                except:
                    message_bit = u'произошла ошибка, при отправке письма с работой'
                else:
                    q.status = '4'
                    message_bit = u'работа отправлена'
                    q.save()
            elif not q.work:
                message_bit = u'работа не загружена(заказ id: %s)' % q.id
            else:
                message_bit = u'заказ(id: %s) не оплачен' % q.id
        self.message_user(request, message_bit)
    send_work.short_description = u'Выслать работу'


class WorkAdmin(admin.ModelAdmin):
    list_display = ('id', 'work', 'title', 'content', 'private')
    list_filter = ('private',)
    search_fields = ['theme', 'content']

class OrderDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'theme', 'order', 'user_email')
    list_filter = ('order',)

    def user_email(self, obj):
        try:
            obj.order.user.email
        except:
            return None
        else:
            return obj.order.user.email
    user_email.short_description = 'email'

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderData, OrderDataAdmin)
admin.site.register(Work, WorkAdmin)
admin.site.register(UserProfile)