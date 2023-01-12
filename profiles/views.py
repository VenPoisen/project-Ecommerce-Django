from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView
from django.views import View
from django.http import HttpResponse
from . import models, forms
import copy


class BaseProfile(View):
    template_name = 'profiles/create.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.cart = copy.deepcopy(self.request.session.get('cart', {}))

        self.profile = None
        self.address = None

        if self.request.user.is_authenticated:
            self.template_name = 'profiles/update.html'

            self.profile = models.Profile.objects.filter(
                user=self.request.user).first()
            self.address = models.Address.objects.filter(
                user=self.profile).all()

            # For now using the first address to show up in the form.
            instance_address = self.address.first()

            # TODO: the idea is to show all the adresses using a for like this one:
            # for i in range(0, self.address.count()):
            #     print(self.address[i])

            self.context = {
                'userform': forms.UserForm(data=self.request.POST or None, user=self.request.user, instance=self.request.user,),
                'profileform': forms.ProfileForm(data=self.request.POST or None, instance=self.profile),
                # Must pass the 'instance=' in the POST addressform as well. Otherwise a new address will be created, rather than updating the old one. # TODO: observation for creating multiple addresses.
                'addressform': forms.AddressForm(data=self.request.POST or None, instance=instance_address),
            }
        else:
            self.context = {
                'userform': forms.UserForm(data=self.request.POST or None),
                'profileform': forms.ProfileForm(data=self.request.POST or None),
                'addressform': forms.AddressForm(data=self.request.POST or None),

            }

        self.userform = self.context['userform']
        self.profileform = self.context['profileform']
        self.addressform = self.context['addressform']

        self.render = render(self.request, self.template_name, self.context)

    def get(self, *args, **kwargs):
        return self.render


class Create(BaseProfile):
    def post(self, *args, **kwargs):

        if not self.userform.is_valid() or not self.profileform.is_valid() or not self.addressform.is_valid():
            messages.error(
                self.request,
                'There are errors in the register form. Check if all fields have been filled correctly.'
            )
            return render(self.request, self.template_name, self.context)

        username = self.userform.cleaned_data.get('username')
        password = self.userform.cleaned_data.get('password')
        email = self.userform.cleaned_data.get('email')
        first_name = self.userform.cleaned_data.get('first_name')
        last_name = self.userform.cleaned_data.get('last_name')
        address_data = self.addressform.cleaned_data

        cpf_data = self.profileform.cleaned_data.get('cpf')
        cpf_db = models.Profile.objects.filter(cpf=cpf_data).first()

        if self.request.user.is_authenticated:
            user = get_object_or_404(User, username=self.request.user.username)
            user.username = username

            if password:
                user.set_password(password)

            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            if cpf_db:
                if str(cpf_db) != str(self.profile.user):
                    messages.error(
                        self.request, 'CPF is already registered.')
                    return redirect('profiles:create')

            if not self.profile:
                self.profileform.cleaned_data['user'] = user
                profile = models.Profile(**self.profileform.cleaned_data)
                profile.save()
            else:
                profile = self.profileform.save(commit=False)
                profile.user = user
                profile.save()

            if not self.address:
                self.addressform.cleaned_data['user'] = self.profile
                address = models.Address(**self.addressform.cleaned_data)
                address.save()
            else:
                address_exists = self.address.filter(
                    address__iexact=address_data['address']).first()

                if address_exists:
                    if address_data['number'] != address_exists.number or address_data['neighborhood'] != address_exists.neighborhood or address_data['cep'] != address_exists.cep or address_data['city'] != address_exists.city or address_data['state'] != address_exists.state:
                        address = self.addressform.save(commit=False)
                        address.user = self.profile
                        address.save()

                else:
                    address = self.addressform.save(commit=False)
                    address.user = self.profile
                    address.save()

            messages.info(
                self.request,
                'Your profile has been successfully updated'
            )

            if self.request.session.get('cart'):
                return redirect('products:checkout')

        else:
            if cpf_db:
                messages.error(
                    self.request, 'The CPF is already registered.')
                return render(self.request, self.template_name, self.context)

            user = self.userform.save(commit=False)
            user.set_password(password)
            user.save()

            profile = self.profileform.save(commit=False)
            profile.user = user
            profile.save()

            address = self.addressform.save(commit=False)
            address.user = profile
            address.save()

            messages.info(
                self.request,
                'Your profile has been successfully created'
            )

        if password:
            authentica = authenticate(
                self.request,
                username=username,
                password=password
            )

            if authentica:
                login(self.request, user=user)

        self.request.session['cart'] = self.cart
        self.request.session.save()

        if self.request.session['cart']:
            return redirect('products:cart')
        return self.render


class Login(View):
    def post(self, *args, **kwargs):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')

        if not username or not password:
            messages.error(
                self.request,
                'Invalid username or password'
            )
            return redirect('profiles:create')

        user = authenticate(self.request, username=username, password=password)

        if not user:
            messages.error(
                self.request,
                'Invalid username or password'
            )
            return redirect('profiles:create')

        login(self.request, user=user)

        if self.request.session.get('cart'):
            messages.info(
                self.request,
                'Login successful, proceed with your order'
            )
            return redirect('products:cart')

        messages.info(
            self.request,
            'Login successful'
        )
        return redirect('products:list')


class Logout(View):
    def get(self, *args, **kwargs):
        cart = copy.deepcopy(self.request.session.get('cart', {}))

        logout(self.request)

        self.request.session['cart'] = cart
        self.request.session.save()

        return redirect('products:list')
