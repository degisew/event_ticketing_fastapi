import qrcode
from io import BytesIO


def generate_qr_code(ticket_info: str):
    qr = qrcode.make(ticket_info)
    img_io = BytesIO()
    qr.save(img_io, format="PNG")
    img_io.seek(0)
    return img_io
