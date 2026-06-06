"""URL Encoder and Decoder."""


def encode_url(text):
    """URL-encode the given text."""
    if not text:
        raise ValueError("Input is empty")
    return __import__('urllib.parse').quote(text, safe='')


def decode_url(text):
    """URL-decode the given text."""
    if not text:
        raise ValueError("Input is empty")
    try:
        return __import__('urllib.parse').unquote(text)
    except Exception as e:
        raise ValueError(f"Invalid URL encoding: {e}")
