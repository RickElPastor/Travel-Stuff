from stellar_model import ModeloEvolutivoEstelar


class ModeloEstelarHibrido(ModeloEvolutivoEstelar):
    nombre = "Modelo estelar híbrido"

    def __init__(
        self,
        modelo_popiii,
        modelo_sevn,
    ):
        self.modelo_popiii = modelo_popiii
        self.modelo_sevn = modelo_sevn

    def seleccionar_modelo(
        self,
        masa_inicial,
        metalicidad_z,
    ):
        if self.modelo_popiii.admite_estrella(
            masa_inicial,
            metalicidad_z,
        ):
            return self.modelo_popiii

        if self.modelo_sevn.admite_estrella(
            masa_inicial,
            metalicidad_z,
        ):
            return self.modelo_sevn

        return None

    def admite_estrella(
        self,
        masa_inicial,
        metalicidad_z,
    ):
        return (
            self.seleccionar_modelo(
                masa_inicial,
                metalicidad_z,
            )
            is not None
        )

    def motivo_no_admitida(
        self,
        masa_inicial,
        metalicidad_z,
    ):
        if metalicidad_z == 0:
            return self.modelo_popiii.motivo_no_admitida(
                masa_inicial,
                metalicidad_z,
            )

        return self.modelo_sevn.motivo_no_admitida(
            masa_inicial,
            metalicidad_z,
        )

    def obtener_estado(
        self,
        masa_inicial,
        metalicidad_z,
        edad,
    ):
        modelo = self.seleccionar_modelo(
            masa_inicial,
            metalicidad_z,
        )

        if modelo is None:
            raise ValueError(
                self.motivo_no_admitida(
                    masa_inicial,
                    metalicidad_z,
                )
            )

        return modelo.obtener_estado(
            masa_inicial=masa_inicial,
            metalicidad_z=metalicidad_z,
            edad=edad,
        )

    def cerrar(self):
        for modelo in (
            self.modelo_popiii,
            self.modelo_sevn,
        ):
            cerrar = getattr(
                modelo,
                "cerrar",
                None,
            )

            if callable(cerrar):
                cerrar()
