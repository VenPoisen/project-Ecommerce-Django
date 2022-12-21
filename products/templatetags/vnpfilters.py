from django.template import Library
from utils import utils

register = Library()


@register.filter
def price_format(value):
    return utils.price_format(value)
