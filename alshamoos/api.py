from io import BytesIO
from base64 import b64encode
import base64
import barcode
import qrcode
from barcode.writer import ImageWriter
from PIL import Image
import zbar
import frappe


@frappe.whitelist()
def get_barcode(data: str) -> str:
    barcode_bytes = get_barcode_bytes(data, format="PNG")
    base_64_string = bytes_to_base64_string(barcode_bytes)

    return add_file_info(base_64_string, "image/png")


@frappe.whitelist()
def get_qr_code(data: str) -> str:
    qr_code_bytes = get_qr_code_bytes(data, format="PNG")
    base_64_string = bytes_to_base64_string(qr_code_bytes)

    return add_file_info(base_64_string, "image/png")


def add_file_info(data: str, mime_type: str) -> str:
    """Add info about the file type and encoding.

    This is required so the browser can make sense of the data."""
    return f"data:{mime_type};base64, {data}"


def get_barcode_bytes(data, format: str) -> bytes:
    """Create a barcode and return the bytes."""

    barcode_class = barcode.get_barcode_class("code128")
    barcode_instance = barcode_class(data, writer=ImageWriter())
    barcode_image = barcode_instance.render()

    buffered = BytesIO()
    barcode_image.save(buffered, format=format)

    return buffered.getvalue()


def get_qr_code_bytes(data, format: str) -> bytes:
    """Create a QR code and return the bytes."""
    img = qrcode.make(data)

    buffered = BytesIO()
    img.save(buffered, format=format)

    return buffered.getvalue()


def bytes_to_base64_string(data: bytes) -> str:
    """Convert bytes to a base64 encoded string."""
    return b64encode(data).decode("utf-8")


@frappe.whitelist()
def add_barcode(barcode, docname):
    # try:
    doc = frappe.get_doc("Item", docname)

    doc.append("barcodes", {"barcode": barcode})

    frappe.set_value(
        "Item Barcode Generator Counter",
        "Item Barcode Generator Counter",
        "barcode_counter",
        int(
            frappe.get_value(
                "Item Barcode Generator Counter",
                "Item Barcode Generator Counter",
                "barcode_counter",
            )
        )
        + 1,
    )

    doc.save()

    frappe.db.commit()

    return "Done!"
    # except:
    # frappe.throw('تأكّد من بيانات الصنف في النظام!')


@frappe.whitelist()
def scan_barcode(doc):
    base64_string = frappe.get_doc("Barcode Generator", doc).barcode_code

    # Decode the base64 string into bytes
    image_bytes = base64.b64decode(base64_string.split(",")[1])

    # Load the bytes as an image using PIL
    image = Image.open(BytesIO(image_bytes))

    # Convert the image to grayscale
    image = image.convert("L")

    # Create a barcode scanner
    scanner = zbar.Scanner()

    # Scan the image for barcodes
    results = scanner.scan(image)

    # Return the barcode data
    if results:
        return results[0].data.decode("utf-8")
