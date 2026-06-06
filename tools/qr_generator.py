"""QR Code Generator - returns base64 PNG."""

import io
import base64


def generate_qr(text, size=10):
    """Generate a QR code and return as base64-encoded PNG."""
    if not text:
        raise ValueError("Input text is empty")

    import qrcode
    from PIL import Image

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=size,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Convert to base64
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    img_b64 = base64.b64encode(buffer.read()).decode('utf-8')

    return {
        'base64': f'data:image/png;base64,{img_b64}',
        'size': img.size,
    }
