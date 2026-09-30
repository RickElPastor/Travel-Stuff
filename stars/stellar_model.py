from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class EstadoEstelar:
    masa_actual: float
    etapa: str
    viva: bool

    edad_modelo_anios: Optional[float] = None

    temperatura_efectiva: Optional[float] = None
    luminosidad: Optional[float] = None
    radio: Optional[float] = None

    masa_nucleo_helio: Optional[float] = None
    masa_nucleo_carbono_oxigeno: Optional[float] = None

    tipo_espectral: Optional[str] = None

    tipo_remanente: Optional[str] = None
    masa_remanente: Optional[float] = None


class ModeloEvolutivoEstelar(ABC):
    nombre = "modelo_no_definido"

    @abstractmethod
    def obtener_estado(
        self,
        masa_inicial,
        metalicidad_z,
        edad,
    ):
        raise NotImplementedError
