"""Color Converter: HEX, RGB, HSL."""

import re


def convert_color(color):
    """Convert a color string to HEX, RGB, and HSL."""
    if not color:
        raise ValueError("Color is empty")

    color = color.strip()

    # Try parsing as HEX
    if color.startswith('#') or (len(color) in (3, 6) and all(c in '0123456789abcdefABCDEF' for c in color)):
        return _from_hex(color)

    # Try parsing as rgb()/rgba()
    if color.lower().startswith('rgb'):
        return _from_rgb_str(color)

    # Try parsing as hsl()/hsla()
    if color.lower().startswith('hsl'):
        return _from_hsl_str(color)

    raise ValueError(f"Unrecognized color format: {color}")


def _from_hex(hex_color):
    hex_color = hex_color.strip().lstrip('#')
    if len(hex_color) == 3:
        hex_color = ''.join(c * 2 for c in hex_color)
    if len(hex_color) != 6:
        raise ValueError(f"Invalid HEX color: #{hex_color}")

    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    return _build_result(r, g, b)


def _from_rgb_str(rgb_str):
    m = re.match(r'rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)', rgb_str)
    if not m:
        raise ValueError(f"Invalid RGB format: {rgb_str}")
    r, g, b = int(m.group(1)), int(m.group(2)), int(m.group(3))
    for v in (r, g, b):
        if not 0 <= v <= 255:
            raise ValueError(f"RGB values must be 0-255, got {v}")
    return _build_result(r, g, b)


def _from_hsl_str(hsl_str):
    m = re.match(r'hsla?\(\s*([\d.]+)\s*,\s*([\d.]+)%?\s*,\s*([\d.]+)%?', hsl_str)
    if not m:
        raise ValueError(f"Invalid HSL format: {hsl_str}")
    h = float(m.group(1)) % 360
    s = float(m.group(2)) / 100
    l = float(m.group(3)) / 100
    r, g, b = _hsl_to_rgb(h, s, l)
    return _build_result(r, g, b)


def _hsl_to_rgb(h, s, l):
    """Convert HSL (h in 0-360, s and l in 0-1) to RGB (0-255)."""
    c = (1 - abs(2 * l - 1)) * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = l - c / 2

    if h < 60:
        r1, g1, b1 = c, x, 0
    elif h < 120:
        r1, g1, b1 = x, c, 0
    elif h < 180:
        r1, g1, b1 = 0, c, x
    elif h < 240:
        r1, g1, b1 = 0, x, c
    elif h < 300:
        r1, g1, b1 = x, 0, c
    else:
        r1, g1, b1 = c, 0, x

    r = round((r1 + m) * 255)
    g = round((g1 + m) * 255)
    b = round((b1 + m) * 255)
    return r, g, b


def _rgb_to_hsl(r, g, b):
    """Convert RGB (0-255) to HSL (h: 0-360, s: 0-100, l: 0-100)."""
    r1, g1, b1 = r / 255, g / 255, b / 255
    c_max = max(r1, g1, b1)
    c_min = min(r1, g1, b1)
    delta = c_max - c_min

    l = (c_max + c_min) / 2

    if delta == 0:
        h = 0
        s = 0
    else:
        s = delta / (1 - abs(2 * l - 1))
        if c_max == r1:
            h = 60 * (((g1 - b1) / delta) % 6)
        elif c_max == g1:
            h = 60 * (((b1 - r1) / delta) + 2)
        else:
            h = 60 * (((r1 - g1) / delta) + 4)

    return round(h, 2), round(s * 100, 2), round(l * 100, 2)


def _build_result(r, g, b):
    hex_val = f'#{r:02x}{g:02x}{b:02x}'
    h, s, l = _rgb_to_hsl(r, g, b)
    return {
        'hex': hex_val.upper(),
        'hex_lower': hex_val,
        'rgb': f'rgb({r}, {g}, {b})',
        'rgb_values': {'r': r, 'g': g, 'b': b},
        'hsl': f'hsl({h}, {s}%, {l}%)',
        'hsl_values': {'h': h, 's': s, 'l': l},
    }
