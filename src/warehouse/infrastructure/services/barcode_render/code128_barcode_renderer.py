# C09: Entorno virtual

from pathlib import Path
import barcode
from barcode.writer import ImageWriter


class Code128BarcodeRenderer:

    def __init__(self, output_dir: str | Path):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def render(self, barcode_value: str) -> str:
        # 1. Validar que el código de barras no esté vacío
        clean_barcode = barcode_value.strip() if barcode_value else ""

        if not clean_barcode:
            raise ValueError(
                "El código de barras no puede estar vacío ni contener solo espacios."
            )

        # 2. Definir la ruta completa esperada (con .png) para verificar existencia
        expected_file = self.output_dir / f"{clean_barcode}.png"

        # 3. Comprobar si ya existe para reutilizarlo
        if expected_file.exists():
            return str(expected_file)

        # 4. Si no existe, construir la ruta base (sin .png) para python-barcode
        file_path_base = self.output_dir / clean_barcode

        # 5. Generar y guardar la nueva imagen
        code128 = barcode.get("code128", clean_barcode, writer=ImageWriter())
        saved_file = code128.save(str(file_path_base))

        return saved_file