from models import db, Mesa
from enums import StatusMesa


def get_todas():
    return Mesa.query.all()

def get_por_id(mesa_id):
    return Mesa.query.get(mesa_id)

def get_livres():
    return Mesa.query.filter_by(status=StatusMesa.LIVRE).all()

def ocupar(mesa_id):
    mesa = get_por_id(mesa_id)
    if not mesa or mesa.status != StatusMesa.LIVRE:
        return False, "Mesa indisponível."
    mesa.status = StatusMesa.OCUPADA
    db.session.commit()
    return True, f"Mesa {mesa.numero} ocupada."

def liberar(mesa_id):
    mesa = get_por_id(mesa_id)
    if not mesa:
        return False, "Mesa não encontrada."
    mesa.status = StatusMesa.LIVRE
    db.session.commit()
    return True, f"Mesa {mesa.numero} liberada."