def formatear_identificador(valor):
    if valor is None:
        return "sin datos"

    return str(valor).replace("_", " ")
