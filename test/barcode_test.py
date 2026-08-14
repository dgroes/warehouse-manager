import barcode
from barcode.writer import ImageWriter

import sys
from pathlib import Path

root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path / "src"))

from warehouse.infrastructure.services.barcode_render.code128_barcode_renderer import (
    Code128BarcodeRenderer,
)

print("BARCODE 128 TEST")
renderer = Code128BarcodeRenderer(
    output_dir=root_path / "data" / "barcodes"
)

codigo_test = "2227118753"

barcode_render = renderer.render(codigo_test)