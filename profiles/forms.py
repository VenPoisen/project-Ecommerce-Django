from utils import addressgenerator
from django import forms
from django.contrib.auth.models import User
from datetime import date
from . import models
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Row, Column, Button


today = date.today()


class ProfileForm(forms.ModelForm):
    birth_date = forms.DateField(widget=forms.DateInput(
        attrs={'type': 'date', 'max': today}), required=True, label='Birth Date')

    cpf = forms.CharField(
        max_length=11, help_text='CPF only numbers', label='CPF')

    class Meta:
        model = models.Profile
        fields = '__all__'
        exclude = ('user',)


class AddressForm(forms.ModelForm):
    class Meta:
        model = models.Address
        fields = '__all__'
        exclude = ('user',)

    address = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    number = forms.CharField(max_length=8, required=False)
    complement = forms.CharField(required=False)
    neighborhood = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    city = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={'readonly': 'readonly'}))
    state = forms.CharField(max_length=2, widget=forms.TextInput(
        attrs={'readonly': 'readonly'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(Fieldset(
            "",
            Row(
                Column('cep', css_class='col'),
                Column(Button(
                    'submit', 'Find CEP', css_class='btn btn-danger text-white col-md-auto mb-button-cep btn-md', onclick='getCEP()',
                )),
                css_class=' justify-content-between'
            ),
            'address',
            'number',
            'complement',
            'neighborhood',
            'city',
            'state',
        ),
            Submit('submit', 'Update',
                   css_class='btn btn-danger text-white btn-block btn-lg')
        )

    field_order = ['cep',]


class CEPForm(forms.ModelForm):
    class Meta:
        model = models.Address
        fields = '__all__'
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_show_labels = False


class UserForm(forms.ModelForm):
    email = forms.EmailField(label='Email Address')
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
    )

    password_confirm = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Password Confirmation'
    )

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = user

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',
                  'password', 'password_confirm', 'email')

    def clean(self, *args, **kwargs):
        data = self.data
        cleaned = self.cleaned_data
        validation_error_msgs = {}

        user_data = cleaned.get('username')
        email_data = cleaned.get('email')
        password_data = cleaned.get('password')
        password_confirm_data = cleaned.get('password_confirm')

        user_db = User.objects.filter(username=user_data).first()
        email_db = User.objects.filter(email=email_data).first()

        error_msg_user_exists = 'User already exists'
        error_msg_email_exists = 'E-mail already exists'
        error_msg_required_field = 'This field is required.'
        error_msg_password_short = 'Password needs at least 6 characters'
        error_msg_password_match = 'Password confirmation do not match'

        if self.user:
            if user_db:
                if user_data == str(self.user):
                    pass
                else:
                    validation_error_msgs['username'] = error_msg_user_exists

            if not email_data:
                validation_error_msgs['email'] = error_msg_required_field

            if email_db:
                if email_data == str(self.user.email):
                    pass
                else:
                    validation_error_msgs['email'] = error_msg_email_exists

            if password_data:
                if password_data != password_confirm_data:
                    validation_error_msgs['password_confirm'] = error_msg_password_match

                if len(password_data) < 6:
                    validation_error_msgs['password'] = error_msg_password_short

        else:
            if user_db:
                validation_error_msgs['username'] = error_msg_user_exists

            if not email_data:
                validation_error_msgs['email'] = error_msg_required_field

            if email_db:
                validation_error_msgs['email'] = error_msg_email_exists

            if not password_data:
                validation_error_msgs['password'] = error_msg_required_field

            elif len(password_data) < 6:
                validation_error_msgs['password'] = error_msg_password_short

            if password_data != password_confirm_data:
                validation_error_msgs['password_confirm'] = error_msg_password_match

        if validation_error_msgs:
            raise (forms.ValidationError(validation_error_msgs))
