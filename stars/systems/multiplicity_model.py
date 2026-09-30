import random


class ModeloMultiplicidadEstelar:
    nombre = "Multiplicidad empírica por masa primaria"

    def obtener_probabilidad_multiple(
        self,
        masa_primaria,
    ):
        masa = float(masa_primaria)

        if masa <= 0:
            raise ValueError("La masa primaria debe ser mayor que 0.")

        # Duchêne & Kraus (2013).
        #
        # Los valores de alta masa son límites
        # inferiores observacionales.
        #
        # Los huecos entre rangos publicados se
        # interpolan de forma aproximada.

        if masa < 0.1:
            return 0.22

        if masa < 0.5:
            return 0.26

        if masa < 0.7:
            return self._interpolar(
                masa,
                0.5,
                0.7,
                0.26,
                0.44,
            )

        if masa < 1.3:
            return 0.44

        if masa < 1.5:
            return self._interpolar(
                masa,
                1.3,
                1.5,
                0.44,
                0.50,
            )

        if masa < 5.0:
            return 0.50

        if masa < 8.0:
            return self._interpolar(
                masa,
                5.0,
                8.0,
                0.50,
                0.60,
            )

        if masa < 16.0:
            return 0.60

        return 0.80

    def es_multiple(
        self,
        seed,
        identificador,
        masa_primaria,
    ):
        probabilidad = self.obtener_probabilidad_multiple(masa_primaria)

        semilla_local = f"{int(seed)}:" f"{identificador}:" "multiplicidad"

        rng = random.Random(semilla_local)

        return rng.random() < probabilidad

    def _interpolar(
        self,
        valor,
        minimo,
        maximo,
        resultado_minimo,
        resultado_maximo,
    ):
        fraccion = (valor - minimo) / (maximo - minimo)

        return resultado_minimo + fraccion * (resultado_maximo - resultado_minimo)
