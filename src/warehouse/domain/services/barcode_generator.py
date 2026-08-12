# BarcodeGenerator -> "Sé generar un barcode a partir de un ID"
from abc import ABC, abstractmethod


class BarcodeGenerator(ABC):

    @abstractmethod
    def generate(self) -> str:
        pass


# BarcodeGenerator
#        │
#        │ contrato
#        ▼
# RandomBarcodeGenerator
#        │
#        └── generate() → "..."