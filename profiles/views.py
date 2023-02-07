from crispy_forms.templatetags.crispy_forms_filters import as_crispy_field
from django.http import JsonResponse
from utils import addressgenerator
from .forms import AddressForm
from django.views.generic import ListView, UpdateView
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView
from django.views import View
from django.http import HttpResponseNotFound, HttpResponse
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

            self.address_id = kwargs.get("pk", None)
            self.address_filter = self.address.filter(
                id=self.address_id).first()

            self.context = {
                'userform': forms.UserForm(data=self.request.POST or None, user=self.request.user, instance=self.request.user,),
                'profileform': forms.ProfileForm(data=self.request.POST or None, instance=self.profile),
                'addressform': forms.AddressForm(data=self.request.POST or None),
                'addresses': self.address,
                'addressdetails': forms.AddressForm(
                    data=self.request.POST or None, instance=self.address_filter),
            }

            self.addressdetails = self.context['addressdetails']

        else:
            self.context = {
                'userform': forms.UserForm(data=self.request.POST or None),
                'profileform': forms.ProfileForm(data=self.request.POST or None),
                'addressform': forms.AddressForm(data=self.request.POST or None),
            }

        self.userform = self.context['userform']
        self.profileform = self.context['profileform']
        self.addressform = self.context['addressform']

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name, self.context)


class Create(BaseProfile):
    def post(self, *args, **kwargs):

        if (not self.userform.is_valid() or not self.profileform.is_valid()) and not self.request.user.is_authenticated:
            messages.error(
                self.request,
                'There are errors in the register form. Check if all fields have been filled correctly.'
            )
            return render(self.request, 'profiles/register.html', self.context)

        if not self.userform.is_valid() or not self.profileform.is_valid():
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

            messages.info(
                self.request,
                'Your profile has been successfully updated'
            )

            if self.request.session.get('cart'):
                return redirect('products:checkout')
            return self.render

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
                messages.info(
                    self.request,
                    'Please add your first address to your profile.'
                )
                return redirect('profiles:address')
        # TODO: em vez de redirecionar p um monte de lugar, criar um template do dashboard com os links?
        self.request.session['cart'] = self.cart
        self.request.session.save()

        self.render = render(self.request, self.template_name, self.context)

        if self.request.session['cart']:
            return redirect('products:cart')
        return self.render


class DispatchLoginRequired(View):
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('profiles:create')

        return super().dispatch(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        profile = models.Profile.objects.filter(
            user=self.request.user).first()
        qs = qs.filter(user=profile)
        return qs


class AddressUpdate(DispatchLoginRequired, BaseProfile):
    address_template_name = 'profiles/updateaddress.html'

    def get(self, *args, **kwargs):
        if not self.address_filter:
            return HttpResponseNotFound()

        return render(self.request, self.address_template_name, self.context)

    def post(self, request, *args, **kwargs):

        if not self.addressdetails.is_valid():
            messages.error(
                self.request,
                'There are errors in the register form. Check if all fields have been filled correctly.'
            )
            return render(self.request, self.address_template_name, self.context)

        self.address_data = self.addressdetails.cleaned_data

        if self.request.user.is_authenticated:

            if not self.address:
                self.addressdetails.cleaned_data['user'] = self.profile
                address = models.Address(**self.addressdetails.cleaned_data)
                address.save()
            else:
                address_exists = self.address.filter(
                    cep__iexact=self.address_data['cep'], number__iexact=self.address_data['number']
                ).first()

                if address_exists:
                    if self.address_data['complement'] != address_exists.complement:
                        address = self.addressdetails.save(commit=False)
                        address.user = self.profile
                        address.save()

                        messages.info(
                            self.request,
                            'Your address has been successfully updated'
                        )
                    else:
                        messages.warning(
                            self.request,
                            'This address already exists in your profile.'
                        )

                        return redirect('profiles:addressdetails', self.address_id)
                else:
                    address = self.addressdetails.save(commit=False)
                    address.user = self.profile
                    address.save()

                    messages.info(
                        self.request,
                        'Your address has been successfully updated'
                    )

            if self.request.session.get('cart'):
                return redirect('products:checkout')

            return redirect('profiles:address')

        else:
            return redirect('profiles:addresscreate')


def cep_update(request, *args, **kwargs):
    if request.method == 'GET':
        form = forms.AddressForm(request.GET)

        cep = request.GET['cep']

        if cep == "":
            return JsonResponse({"cep": "EMPTY CEP"})

        cep_refresher = addressgenerator.address(cep)

        if cep_refresher is None:
            return HttpResponse(as_crispy_field(form['cep']))

        changes = {
            'address': cep_refresher['logradouro'],
            'neighborhood': cep_refresher['bairro'],
            'city': cep_refresher['cidade'],
            'state': cep_refresher['uf'],
        }

        if cep_refresher['complemento'] != "":
            if request.GET['complement'] == "":
                changes.update({'complement': cep_refresher['complemento']})

        return JsonResponse(changes)


class AddressList(DispatchLoginRequired, ListView):
    model = models.Address
    context_object_name = 'addresses'
    template_name = 'profiles/address.html'
    paginate_by = 10
    ordering = ['-id']


class AddressCreate(BaseProfile):
    address_template_name = 'profiles/newaddress.html'

    def get(self, *args, **kwargs):
        return render(self.request, self.address_template_name, self.context)

    def post(self, *args, **kwargs):

        if not self.addressform.is_valid():
            messages.error(
                self.request,
                'There are errors in the register form. Check if all fields have been filled correctly.'
            )
            return render(self.request, self.address_template_name, self.context)

        address = self.addressform.save(commit=False)
        address.user = self.profile
        address.save()

        messages.info(
            self.request,
            'Your address has been successfully created'
        )

        self.request.session['cart'] = self.cart
        self.request.session.save()

        if self.request.session['cart']:
            return redirect('products:cart')
        return redirect('profiles:address')


class AddressDelete(BaseProfile):

    def get(self, *args, **kwargs):
        self.address_filter.delete()

        return redirect('profiles:address')


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
