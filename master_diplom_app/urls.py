# coding:utf-8

from django.conf.urls import patterns, url
from django.views import generic
from django.contrib.auth.decorators import login_required
from views import UserAccountView, IndexView, CreateOrderView, ContactInfoView, OrderDetailView, WorkSamplesVies

urlpatterns = patterns('',
    url(r'account/$', UserAccountView.as_view(), name='user_account'),
    url(r'account/order/(?P<pk>\d+)/$', login_required(OrderDetailView.as_view())),
    url(r'create_order/$', CreateOrderView.as_view(), name='create_order'),
    url(r'get_contact_info/$', ContactInfoView.as_view(), name='get_contact_info'),
    url(r'order_success/$', generic.TemplateView.as_view(template_name='master_diplom/order_success.html')),
    url(r'payment_success/$', generic.TemplateView.as_view(template_name='master_diplom/payment_success.html')),
    url(r'samples/$', WorkSamplesVies.as_view(), name='samples'),
    url(r'comments/$', generic.TemplateView.as_view(template_name='master_diplom/comments.html'), name='comments'),
    url(r'^$', IndexView.as_view(), name='index'),
)