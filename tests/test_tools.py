import pytest, json, hashlib, base64

def test_json_formatter():
    data = {'key': 'value', 'nested': {'a': 1}}
    formatted = json.dumps(data, indent=2)
    assert '"key"' in formatted

def test_hash_generator():
    result = hashlib.sha256(b'test').hexdigest()
    assert len(result) == 64

def test_base64_roundtrip():
    original = b'hello world'
    encoded = base64.b64encode(original)
    decoded = base64.b64decode(encoded)
    assert decoded == original

def test_jwt_structure():
    import base64
    h = base64.b64encode(json.dumps({'alg': 'HS256'}).encode()).decode()
    p = base64.b64encode(json.dumps({'sub': 'test'}).encode()).decode()
    jwt = f'{h}.{p}.sig'
    assert len(jwt.split('.')) == 3
