def calculator(cep):
    base_price = 5
    base_cep = "38400000"

    if not cep:
        return None

    if cep[0] == base_cep[0]:
        if cep[1] == base_cep[1]:
            return base_price
        base_price += 3.30
        return base_price

    elif cep[0] == "0":
        base_price += 6.40
        return base_price

    elif cep[0] == "1" or cep[0] == "2" or cep[0] == "4":
        if cep[0] == "1" and 1 < int(cep[1]) < 6:
            base_price += 3.30
            return base_price
        elif cep[0] == "4" and 4 < int(cep[1]) < 8 or cep[0] == "2":
            base_price += 6.40
            return base_price
        base_price += 10.40
        return base_price

    elif cep[0] == "5" or cep[0] == "8" or cep[0] == "9":
        base_price += 24.40
        return base_price

    elif cep[0] == "6":
        base_price += 34.40
        return base_price

    elif cep[0] == "7":
        if int(cep[1]) < 6:
            base_price += 3.30
            return base_price
        base_price += 14.40
        return base_price

    else:
        return None
