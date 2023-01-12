from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
from utils.validacpf import valida_cpf
import re


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField()
    birth_date = models.DateField()
    cpf = models.CharField(max_length=11, help_text='CPF only numbers')

    def __str__(self):
        return f'{self.user}'

    def clean(self):
        error_msgs = {}

        cpf_form = self.cpf or None
        cpf_save = None
        profile = Profile.objects.filter(cpf=cpf_form).first()

        if profile:
            cpf_save = profile.cpf

            if cpf_save is not None and self.pk != profile.pk:
                error_msgs['cpf'] = 'CPF already exists.'

        if not valida_cpf(self.cpf):
            error_msgs['cpf'] = 'Type a valid CPF'

        if error_msgs:
            raise ValidationError(error_msgs)


class Address(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    address = models.CharField(max_length=50)
    number = models.CharField(max_length=8)
    complement = models.CharField(max_length=30, blank=True, null=True)
    neighborhood = models.CharField(max_length=30)
    cep = models.CharField(max_length=8, help_text='CEP only numbers')
    city = models.CharField(max_length=30)
    state = models.CharField(
        default='SP',
        max_length=2,
        choices=(
            ('AC', 'Acre'),
            ('AL', 'Alagoas'),
            ('AP', 'Amapá'),
            ('AM', 'Amazonas'),
            ('BA', 'Bahia'),
            ('CE', 'Ceará'),
            ('DF', 'Distrito Federal'),
            ('ES', 'Espírito Santo'),
            ('GO', 'Goiás'),
            ('MA', 'Maranhão'),
            ('MT', 'Mato Grosso'),
            ('MS', 'Mato Grosso do Sul'),
            ('MG', 'Minas Gerais'),
            ('PA', 'Pará'),
            ('PB', 'Paraíba'),
            ('PR', 'Paraná'),
            ('PE', 'Pernambuco'),
            ('PI', 'Piauí'),
            ('RJ', 'Rio de Janeiro'),
            ('RN', 'Rio Grande do Norte'),
            ('RS', 'Rio Grande do Sul'),
            ('RO', 'Rondônia'),
            ('RR', 'Roraima'),
            ('SC', 'Santa Catarina'),
            ('SP', 'São Paulo'),
            ('SE', 'Sergipe'),
            ('TO', 'Tocantins'),
        ),
    )

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    def clean(self):
        error_msgs = {}

        if re.search(r'[^0-9]', self.cep) or len(self.cep) < 8:
            error_msgs['cep'] = 'invalid CEP, type all and only numbers'

        if error_msgs:
            raise ValidationError(error_msgs)
