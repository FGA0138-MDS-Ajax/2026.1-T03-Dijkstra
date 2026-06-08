from enums import StatusMesa


def ocupar(mesa):
    if mesa.status != StatusMesa.LIVRE:
        return False, f"Mesa {mesa.numero} não está livre."
    mesa.status = StatusMesa.OCUPADA
    return True, f"Mesa {mesa.numero} ocupada."

def liberar(mesa):
    mesa.status = StatusMesa.LIVRE
    return True, f"Mesa {mesa.numero} liberada."