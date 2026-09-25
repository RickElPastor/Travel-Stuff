from functools import lru_cache

import astropy.units as u
from astropy.cosmology import Planck18, z_at_value


class CosmologiaPlanck18:
    REDSHIFT_MAX_FORMACION_ESTELAR = 24.0

    def __init__(self):
        self.modelo = Planck18

        self.edad_actual_anios = float(self.modelo.age(0).to_value(u.yr))

        self.edad_minima_formacion_anios = float(
            self.modelo.age(self.REDSHIFT_MAX_FORMACION_ESTELAR).to_value(u.yr)
        )

    @lru_cache(maxsize=20_000)
    def redshift_desde_edad(self, edad_anios):
        edad_anios = float(edad_anios)

        if edad_anios <= 0:
            return None

        if edad_anios < self.edad_minima_formacion_anios:
            return None

        if edad_anios > self.edad_actual_anios:
            return None

        redshift = z_at_value(
            self.modelo.age,
            edad_anios * u.yr,
            zmin=0.0,
            zmax=self.REDSHIFT_MAX_FORMACION_ESTELAR,
        )

        return float(redshift.value)

