class SistemaEstelar:
    def __init__(
        self,
        nombre,
        anio_formacion,
        estrellas=None,
        estrella_primaria=None,
        periodo_orbital_dias=None,
        semieje_mayor_au=None,
        excentricidad=None,
        q_objetivo=None,
        q_real=None,
    ):
        self.nombre = str(nombre)
        self.anio_formacion = int(anio_formacion)

        self.nombres_estrellas = []
        self.nombre_estrella_primaria = None

        self.periodo_orbital_dias = (
            None if periodo_orbital_dias is None else float(periodo_orbital_dias)
        )

        self.semieje_mayor_au = (
            None if semieje_mayor_au is None else float(semieje_mayor_au)
        )

        self.excentricidad = None if excentricidad is None else float(excentricidad)

        self.q_objetivo = None if q_objetivo is None else float(q_objetivo)

        self.q_real = None if q_real is None else float(q_real)

        if estrellas:
            for estrella in estrellas:
                self.agregar_estrella(estrella)

        if estrella_primaria is not None:
            self.establecer_estrella_primaria(estrella_primaria)

    def _obtener_nombre_estrella(
        self,
        estrella,
    ):
        if hasattr(
            estrella,
            "nombre",
        ):
            return estrella.nombre

        return str(estrella)

    def agregar_estrella(
        self,
        estrella,
    ):
        nombre = self._obtener_nombre_estrella(estrella)

        if nombre not in self.nombres_estrellas:
            self.nombres_estrellas.append(nombre)

    def establecer_estrella_primaria(
        self,
        estrella,
    ):
        nombre = self._obtener_nombre_estrella(estrella)

        self.agregar_estrella(nombre)

        self.nombre_estrella_primaria = nombre

    def actualizar_datos_orbitales(
        self,
        periodo_orbital_dias=None,
        semieje_mayor_au=None,
        excentricidad=None,
        q_objetivo=None,
        q_real=None,
    ):
        if periodo_orbital_dias is not None:
            self.periodo_orbital_dias = float(periodo_orbital_dias)

        if semieje_mayor_au is not None:
            self.semieje_mayor_au = float(semieje_mayor_au)

        if excentricidad is not None:
            self.excentricidad = float(excentricidad)

        if q_objetivo is not None:
            self.q_objetivo = float(q_objetivo)

        if q_real is not None:
            self.q_real = float(q_real)

    def quitar_estrella(
        self,
        estrella,
    ):
        nombre = self._obtener_nombre_estrella(estrella)

        if nombre in self.nombres_estrellas:
            self.nombres_estrellas.remove(nombre)

        if self.nombre_estrella_primaria == nombre:
            self.nombre_estrella_primaria = None

    def obtener_cantidad_estrellas(
        self,
    ):
        return len(self.nombres_estrellas)

    def obtener_tipo(
        self,
    ):
        cantidad = self.obtener_cantidad_estrellas()

        if cantidad == 1:
            return "simple"

        if cantidad == 2:
            return "binario"

        if cantidad == 3:
            return "triple"

        if cantidad > 3:
            return "multiple"

        return "vacio"

    def obtener_periastro_au(self):
        if self.semieje_mayor_au is None or self.excentricidad is None:
            return None

        return self.semieje_mayor_au * (1.0 - self.excentricidad)

    def obtener_apoastro_au(self):
        if self.semieje_mayor_au is None or self.excentricidad is None:
            return None

        return self.semieje_mayor_au * (1.0 + self.excentricidad)

    def a_dict(
        self,
    ):
        return {
            "nombre": self.nombre,
            "anio_formacion": (self.anio_formacion),
            "estrella_primaria": (self.nombre_estrella_primaria),
            "estrellas": list(self.nombres_estrellas),
            "periodo_orbital_dias": (self.periodo_orbital_dias),
            "semieje_mayor_au": (self.semieje_mayor_au),
            "excentricidad": (self.excentricidad),
            "q_objetivo": (self.q_objetivo),
            "q_real": (self.q_real),
        }

    @classmethod
    def desde_dict(
        cls,
        datos,
    ):
        sistema = cls(
            nombre=datos["nombre"],
            anio_formacion=(datos["anio_formacion"]),
            periodo_orbital_dias=(datos.get("periodo_orbital_dias")),
            semieje_mayor_au=(datos.get("semieje_mayor_au")),
            excentricidad=(datos.get("excentricidad")),
            q_objetivo=datos.get("q_objetivo"),
            q_real=datos.get("q_real"),
        )

        for nombre_estrella in datos.get(
            "estrellas",
            [],
        ):
            sistema.agregar_estrella(nombre_estrella)

        nombre_primaria = datos.get("estrella_primaria")

        if nombre_primaria is not None:
            sistema.establecer_estrella_primaria(nombre_primaria)

        elif sistema.nombres_estrellas:
            sistema.establecer_estrella_primaria(sistema.nombres_estrellas[0])

        return sistema
