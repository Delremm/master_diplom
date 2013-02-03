
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

def send_email(template_name, user, **kwargs):

    ctx_dict = kwargs

    subject = render_to_string('master_diplom/email_templates/payment_notification_subject.txt',
        ctx_dict)
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())

    message = render_to_string(template_name,
        ctx_dict)

    user.email_user(subject, message, 'manager@master-diplom.com')

def send_payment_notification(request, user, **kwargs):
    if Site._meta.installed:
        site = Site.objects.get_current()
    else:
        site = RequestSite(request)
    kwargs['site'] = site

    send_email('master_diplom/email_templates/payment_notification.txt', user, **kwargs)


def send_work(request, user, **kwargs):
    if Site._meta.installed:
        site = Site.objects.get_current()
    else:
        site = RequestSite(request)
    kwargs['site'] = site

    subject = render_to_string("master_diplom/email_templates/work_delivery_subject.txt", kwargs)
    subject = ''.join(subject.splitlines())

    message = render_to_string('master_diplom/email_templates/work_delivery.txt', kwargs)

    email = EmailMessage(subject, message, 'manager@master-diplom.com', [user.email])
    
    order = kwargs['order']

    email.attach_file(order.work.work.path)
    email.send()
