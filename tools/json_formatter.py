"""JSON Formatter, Minifier, and Validator."""


def format_json(text, indent=2):
    """Format JSON with specified indentation."""
    if not text.strip():
        raise ValueError("Input is empty")
    parsed = json_load(text)
    return json_dumps(parsed, indent)


def minify_json(text):
    """Minify JSON by removing whitespace."""
    if not text.strip():
        raise ValueError("Input is empty")
    parsed = json_load(text)
    return json_dumps(parsed)


def validate_json(text):
    """Validate JSON string. Returns (valid, error_message)."""
    if not text.strip():
        return False, "Input is empty"
    try:
        json_load(text)
        return True, None
    except Exception as e:
        return False, str(e)


def json_load(text):
    """Load JSON, handling common issues."""
    text = text.strip()
    if not text:
        raise ValueError("Input is empty")
    try:
        import json as _json
        return _json.loads(text)
    except Exception as e:
        raise ValueError(f"Invalid JSON: {e}")


def json_dumps(obj, indent=None):
    """Dump JSON with optional indentation."""
    import json as _json
    if indent is not None:
        return _json.dumps(obj, indent=indent, ensure_ascii=False)
    return _json.dumps(obj, separators=(',', ':'), ensure_ascii=False)
