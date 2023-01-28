from django.http import JsonResponse
from pycep_correios import get_address_from_cep, exceptions, WebService


def address(cep):
    try:

        address = get_address_from_cep(cep, webservice=WebService.VIACEP)
        return address

    except exceptions.InvalidCEP as eic:
        return None

    except exceptions.CEPNotFound as ecnf:
        return None

    except exceptions.ConnectionError as errc:
        return None

    except exceptions.Timeout as errt:
        return None

    except exceptions.HTTPError as errh:
        return None

    except exceptions.BaseException as e:
        return None
