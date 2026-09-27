import math


class ModeloEstructuraDisco:
    """
    Estructura radial simplificada del polvo.

    Perfil usado:

        Sigma(r) ∝ r^-1 * exp(-r / Rc)

    donde Rc es el radio característico.
    """

    RADIO_CARACTERISTICO_BASE_AU = 30.0

    # Aproximación de Fase 1.
    # Todavía no calculamos sublimación del polvo
    # porque no tenemos la temperatura del disco.
    RADIO_INTERIOR_AU = 0.05

    GAMMA = 1.0

    def calcular_radio_caracteristico_au(
        self,
        masa_estelar,
    ):
        if masa_estelar <= 0:
            raise ValueError("La masa estelar debe ser mayor que 0.")

        return self.RADIO_CARACTERISTICO_BASE_AU * math.sqrt(float(masa_estelar))
