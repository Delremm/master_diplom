# coding:utf-8
from datetime import date

from django.views import generic
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from models import Order, OrderData, UserProfile
from forms import OrderDataForm, ContactsForm

from registration_email.forms import EmailAuthenticationForm

from robokassa.forms import RobokassaForm

class UserAccountView(generic.TemplateView):
    template_name = 'master_diplom/account_detail.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        user = request.user
        if user.is_anonymous():
            return HttpResponseRedirect('/account_doesnt_exists/')
        context['orders'] = user.orders
        return self.render_to_response(context)


class IndexView(generic.TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        #context['user'] = request.user
        return self.render_to_response(context)


class CreateOrderView(generic.TemplateView):
    template_name = 'master_diplom/create_order.html'

    def get_context_data(self, **kwargs):
        context = super(CreateOrderView, self).get_context_data(**kwargs)
        form = OrderDataForm()
        context['form'] = form
        context['date'] = date.strftime(date.today(), "%Y-%m-%d")
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = OrderDataForm(request.POST, request.FILES)
        if form.is_valid():
            data=dict(
                discipline = form.cleaned_data['discipline'],
                type = form.cleaned_data['type'],
                theme = form.cleaned_data['theme'],
                content = form.cleaned_data['content'],
                pages_num = form.cleaned_data['pages_num'],
                cost = form.cleaned_data['cost'],
                deadline = form.cleaned_data['deadline'],
                notes = form.cleaned_data['notes'],
                attached_file=request.FILES.get('attached_file', None)
            )
            order_data = OrderData(**data)
            order_data.save()
            request.session['order_data'] = order_data
            return HttpResponseRedirect('/get_contact_info/')
        context['form'] = form
        return self.render_to_response(context)


import hashlib
from django.contrib.auth import login, authenticate

from registration.signals import user_registered
from registration_email.forms import generate_username
from django.template.loader import render_to_string

from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site


class ContactInfoView(generic.TemplateView):
    template_name = 'master_diplom/contact_info.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if not request.session.get('order_data', 0):
            return HttpResponseRedirect('/create_order/')
        user = request.user
        if user.is_authenticated():
            try:
                profile = user.profiles.all()[0]
                context['profile'] = profile
            except IndexError:
                pass
            context['authenticated'] = True

        else:
            context['login_form'] = True
            form = ContactsForm()
            context['form'] = form
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.user.is_authenticated():
            site = self.get_site(request)
            order_data = request.session.get('order_data', None)
            order = Order(user=request.user)
            order.save()
            order_data.order = order
            order_data.save()
            self.send_email('master_diplom/order_email.txt', request.user, order_id=order.id, site=site)
            return HttpResponseRedirect('/order_success/')
        form = ContactsForm(data=request.POST)
        if form.is_valid():
            email = self.clean_email(form.cleaned_data['email'])
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']

            request.session['order_email'] = email
            email = self.clean_email(email)
            try:
                user = User.objects.get(email__iexact=email)
                if user:
                    context['form_errors'] = 'User with given email already exists, please log in or give another email.'
                    context['form'] = form
                    return self.render_to_response(context)
            except User.DoesNotExist:
                password = hashlib.new('sha1', email).hexdigest()[0:6]
                user = self.register_new_user(request, email, password)
                profile = UserProfile(user=user, name=name, phone=phone)
                profile.save()
                # phone will be saved at user.last_name
                site = self.get_site(request)
                order_data = request.session.get('order_data', None)

                order = Order(user=user)
                order.save()
                order_data.order = order
                order_data.save()
                self.send_registration_email(user, password, order.id, site)
                return HttpResponseRedirect('/order_success/')

            return HttpResponseRedirect('/get_contact_info/')
        context['form'] = form
        return self.render_to_response(context)

    def get_site(self, request):
        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)
        return site

    def send_registration_email(self, user, password, order_id, site):

        ctx_dict = {'email': user.email,
                    'password': password,
                    'order_id': order_id,
                    'site': site
                    }
        subject = render_to_string('master_diplom/email_subject.txt',
            ctx_dict)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())

        message = render_to_string('master_diplom/registration_email.txt',
            ctx_dict)

        user.email_user(subject, message, 'manager@master-diplom.com')

    def send_email(self, template_name, user, **kwargs):

        ctx_dict = kwargs

        subject = render_to_string('master_diplom/email_subject.txt',
            ctx_dict)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())

        message = render_to_string(template_name,
            ctx_dict)

        user.email_user(subject, message, 'manager@master-diplom.com')

    def register_new_user(self, request, email, password):
        """
        Create and immediately log in a new user.

        """
        email, password = email, password
        email = self.clean_email(email)
        username = self.generate_username(email)
        User.objects.create_user(username, email, password)

        # authenticate() always has to be called before login(), and
        # will return the user we just created.
        new_user = authenticate(username=username, password=password)
        login(request, new_user)
        user_registered.send(sender=self.__class__,
            user=new_user,
            request=request)
        return new_user

    def clean_email(self, email):
        """
        Validate that the username is alphanumeric and is not already
        in use.
        """
        try:
            User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return email.lower()
        return None

    def get_md5_hexdigest(self, email):
        """
        Returns an md5 hash for a given email.
        """
        return hashlib.new('md5', email).hexdigest()[0:30]

    def generate_username(self, email):
        """
        Generates a unique username for the given email.

        The username will be an md5 hash of the given email. If the username exists
        we just append `a` to the email until we get a unique md5 hash.
        """
        try:
            User.objects.get(email=email)
            raise Exception('Cannot generate new username. A user with this email'
                        'already exists.')
        except User.DoesNotExist:
            pass

        username = self.get_md5_hexdigest(email)
        found_unique_username = False
        while not found_unique_username:
            try:
                User.objects.get(username=username)
                email = '{0}a'.format(email.lower())
                username = self.get_md5_hexdigest(email)
            except User.DoesNotExist:
                found_unique_username = True
                return username

class OrderDetailView(generic.TemplateView):
    template_name = 'master_diplom/order_detail.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        try:
            order = request.user.orders.get(id=kwargs['pk'])
        except Order.DoesNotExist:
            return HttpResponseRedirect('/account/')
        else:
            form = RobokassaForm(initial={
                'OutSum': order.total,
                'InvId': order.id,
                'Desc': order.order_data.theme,
                'Email': request.user.email,
                # 'IncCurrLabel': '',
                # 'Culture': 'ru'
            })
            context['object'] = order
            context['payment_form'] = form
        return self.render_to_response(context)

