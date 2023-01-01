from django import forms
from django.contrib.auth.models import User
from datetime import date
from . import models

today = date.today()


class ProfileForm(forms.ModelForm):
    birth_date = forms.DateField(widget=forms.TextInput(
        attrs={'value': today, 'type': 'date'}), required=True)

    class Meta:
        model = models.Profile
        fields = '__all__'
        exclude = ('user',)


class AddressForm(forms.ModelForm):
    complement = forms.CharField(required=False)

    class Meta:
        model = models.Address
        fields = '__all__'
        exclude = ('user',)


class UserForm(forms.ModelForm):
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

            if email_db:
                if email_data == str(self.user.email):
                    pass
                else:
                    validation_error_msgs['email'] = error_msg_email_exists

            if not email_data:
                email_data = self.user.email

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
