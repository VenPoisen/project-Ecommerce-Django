from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
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

        if self.request.user.is_authenticated:
            self.profile = models.Profile.objects.filter(
                user=self.request.user).first()

            self.context = {
                'userform': forms.UserForm(data=self.request.POST or None, user=self.request.user, instance=self.request.user,),
                'profileform': forms.ProfileForm(data=self.request.POST or None),
                'addressform': forms.AddressForm(data=self.request.POST or None),
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

        # if not self.userform.is_valid() or not self.profileform.is_valid():
        if not self.userform.is_valid():
            print('Invalid')
            return self.render

        username = self.userform.cleaned_data.get('username')
        password = self.userform.cleaned_data.get('password')
        email = self.userform.cleaned_data.get('email')
        first_name = self.userform.cleaned_data.get('first_name')
        last_name = self.userform.cleaned_data.get('last_name')

        if self.request.user.is_authenticated:
            user = get_object_or_404(User, username=self.request.user.username)
            user.username = username

            if password:
                user.set_password(password)

            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.save()

        else:
            user = self.userform.save(commit=False)
            user.set_password(password)
            user.save()

            profile = self.profileform.save(commit=False)
            profile.user = user
            profile.save()

            address = self.addressform.save(commit=False)
            address.user = profile
            address.save()

        self.request.session['cart'] = self.cart
        self.request.session.save()
        return self.render


class Update(View):
    pass


class Login(View):
    pass


class Logout(View):
    pass
