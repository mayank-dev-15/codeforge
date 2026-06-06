"""JWT Token Decoder (no signature verification)."""

import base64
import json


def decode_jwt(token):
    """Decode a JWT token and return header, payload, and signature."""
    if not token:
        raise ValueError("Token is empty")

    parts = token.strip().split('.')
    if len(parts) != 3:
        raise ValueError("Invalid JWT format: expected 3 parts (header.payload.signature)")

    header = _decode_jwt_part(parts[0], "header")
    payload = _decode_jwt_part(parts[1], "payload")
    signature = parts[2]

    # Add human-readable timestamps
    from datetime import datetime, timezone
    for field in ['exp', 'iat', 'nbf']:
        if field in payload:
            try:
                ts = payload[field]
                dt = datetime.fromtimestamp(ts, tz=timezone.utc)
                payload[f'{field}_readable'] = dt.strftime('%Y-%m-%d %H:%M:%S UTC')
            except (OSError, ValueError, OverflowError):
                pass

    return {
        'header': header,
        'payload': payload,
        'signature': signature,
        'header_json': json.dumps(header, indent=2),
        'payload_json': json.dumps(payload, indent=2),
    }


def _decode_jwt_part(part, name):
    """Decode a single JWT part (base64url encoded JSON)."""
    # Add padding
    missing = len(part) % 4
    if missing:
        part += '=' * (4 - missing)
    try:
        decoded = base64.urlsafe_b64decode(part)
        return json.loads(decoded)
    except Exception as e:
        raise ValueError(f"Invalid JWT {name}: {e}")
