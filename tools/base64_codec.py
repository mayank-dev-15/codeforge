"""Base64 Encoder and Decoder."""


def encode_base64(text):
    """Encode text to Base64."""
    if not text:
        raise ValueError("Input is empty")
    return __import__('base64').b64encode(text.encode('utf-8')).decode('utf-8')


def decode_base64(text):
    """Decode Base64 to text."""
    if not text:
        raise ValueError("Input is empty")
    text = text.strip()
    # Add padding if needed
    missing = len(text) % 4
    if missing:
        text += '=' * (4 - missing)
    try:
        return __import__('base64').b64decode(text).decode('utf-8')
    except Exception as e:
        raise ValueError(f"Invalid Base64: {e}")
