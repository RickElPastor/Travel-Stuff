import random


class ModeloReglasMundo:
    """
    Determina las reglas fundamentales adicionales
    de un planeta.

    La física normal NO se elimina.

    Un mundo extraordinario mantiene sus propiedades
    físicas normales y además puede poseer reglas
    adicionales que otros módulos utilizarán después.

    Las probabilidades de este archivo son decisiones
    de diseño del simulador, NO datos científicos.
    """

    PROBABILIDAD_EXTRAORDINARIO = 0.03

    TIPOS_EXTRAORDINARIOS = (
        "arcano",
        "anomalia_fisica",
        "energia_exotica",
    )

    def asignar(
        self,
        planeta,
        seed,
    ):
        # Solo se decide una vez.
        if planeta.regimen_mundo != "sin_asignar":
            return

        generador = random.Random(f"{seed}:{planeta.nombre}:reglas_mundo")

        valor = generador.random()

        if valor >= self.PROBABILIDAD_EXTRAORDINARIO:
            self._asignar_normal(planeta)
            return

        self._asignar_extraordinario(
            planeta,
            generador,
        )

    def _asignar_normal(
        self,
        planeta,
    ):
        planeta.regimen_mundo = "normal"

        planeta.tipo_regla_extraordinaria = None

        planeta.intensidad_extraordinaria = 0.0

    def _asignar_extraordinario(
        self,
        planeta,
        generador,
    ):
        planeta.regimen_mundo = "extraordinario"

        planeta.tipo_regla_extraordinaria = generador.choice(self.TIPOS_EXTRAORDINARIOS)

        planeta.intensidad_extraordinaria = generador.random()
