from django.contrib import admin
from django.template.defaultfilters import escape
from django.core.urlresolvers import reverse
from django.forms.widgets import Widget
from django.db import models

from models import Order, OrderData, UserProfile



class OrderDataLinkWidget(Widget):
    def render(self, name, value, attrs=None):
        url ="/admin/master_diplom_app/orderdata/%s"%value #or use reverse
        return "<a href='%s'>order data</a>"%(url, )


class OrderAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.OneToOneField: {'widget': OrderDataLinkWidget},
    }


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderData)