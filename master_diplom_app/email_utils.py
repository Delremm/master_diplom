
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site
from django.template.loader import render_to_string

def send_email(template_name, user, **kwargs):

    ctx_dict = kwargs

    subject = render_to_string('master_diplom/email_templates/payment_notification_subject.txt',
        ctx_dict)
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())

    message = render_to_string(template_name,
        ctx_dict)
    print "templateeee: %s" % template_name
    print "user: %s" % user
    print "kwargs: %s" % kwargs
    user.email_user(subject, message, 'master-diplom.com')

def send_payment_notification(request, user, **kwargs):
    if Site._meta.installed:
        site = Site.objects.get_current()
    else:
        site = RequestSite(request)
    kwargs['site'] = site
    print kwargs
    print user.email
    send_email('master_diplom/email_templates/payment_notification.txt', user, **kwargs)