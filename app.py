#!/usr/bin/env python3
"""CodeForge - All-in-One Developer Tools Suite"""

from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import json
import re
import hashlib
import base64
import urllib.parse
import difflib
import secrets
import string
import os
import sys

# Add tools directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tools'))

from json_formatter import format_json, minify_json, validate_json
from regex_tester import test_regex
from hash_generator import generate_hash
from base64_codec import encode_base64, decode_base64
from url_codec import encode_url, decode_url
from jwt_decoder import decode_jwt
from diff_checker import check_diff
from color_picker import convert_color
from lorem_generator import generate_lorem
from qr_generator import generate_qr

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)


# ─── Page Routes ───────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)


# ─── API: JSON Formatter ───────────────────────────────────────────────────────

@app.route('/api/json/format', methods=['POST'])
def api_json_format():
    data = request.get_json()
    text = data.get('text', '')
    indent = data.get('indent', 2)
    action = data.get('action', 'format')
    try:
        if action == 'minify':
            result = minify_json(text)
        else:
            result = format_json(text, indent)
        return jsonify({'success': True, 'result': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/json/validate', methods=['POST'])
def api_json_validate():
    data = request.get_json()
    text = data.get('text', '')
    valid, error = validate_json(text)
    return jsonify({'valid': valid, 'error': error})


# ─── API: Regex Tester ────────────────────────────────────────────────────────

@app.route('/api/regex/test', methods=['POST'])
def api_regex_test():
    data = request.get_json()
    pattern = data.get('pattern', '')
    text = data.get('text', '')
    flags = data.get('flags', '')
    try:
        result = test_regex(pattern, text, flags)
        return jsonify({'success': True, **result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


# ─── API: Hash Generator ──────────────────────────────────────────────────────

@app.route('/api/hash/generate', methods=['POST'])
def api_hash_generate():
    data = request.get_json()
    text = data.get('text', '')
    algorithms = data.get('algorithms', ['md5', 'sha1', 'sha256', 'sha512'])
    try:
        result = generate_hash(text, algorithms)
        return jsonify({'success': True, 'hashes': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


# ─── API: Base64 Codec ────────────────────────────────────────────────────────

@app.route('/api/base64/encode', methods=['POST'])
def api_base64_encode():
    data = request.get_json()
    text = data.get('text', '')
    try:
        result = encode_base64(text)
        return jsonify({'success': True, 'result': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/base64/decode', methods=['POST'])
def api_base64_decode():
    data = request.get_json()
    text = data.get('text', '')
    try:
        result = decode_base64(text)
        return jsonify({'success': True, 'result': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


# ─── API: URL Codec ───────────────────────────────────────────────────────────

@app.route('/api/url/encode', methods=['POST'])
def api_url_encode():
    data = request.get_json()
    text = data.get('text', '')
    try:
        result = encode_url(text)
        return jsonify({'success': True, 'result': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/url/decode', methods=['POST'])
def api_url_decode():
    data = request.get_json()
    text = data.get('text', '')
    try:
        result = decode_url(text)
        return jsonify({'success': True, 'result': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


# ─── API: JWT Decoder ─────────────────────────────────────────────────────────

@app.route('/api/jwt/decode', methods=['POST'])
def api_jwt_decode():
    data = request.get_json()
    token = data.get('token', '')
    try:
        result = decode_jwt(token)
        return jsonify({'success': True, **result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


# ─── API: Diff Checker ────────────────────────────────────────────────────────

@app.route('/api/diff/check', methods=['POST'])
def api_diff_check():
    data = request.get_json()
    text1 = data.get('text1', '')
    text2 = data.get('text2', '')
    try:
        result = check_diff(text1, text2)
        return jsonify({'success': True, 'result': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


# ─── API: Color Picker ────────────────────────────────────────────────────────

@app.route('/api/color/convert', methods=['POST'])
def api_color_convert():
    data = request.get_json()
    color = data.get('color', '')
    try:
        result = convert_color(color)
        return jsonify({'success': True, **result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


# ─── API: Lorem Generator ─────────────────────────────────────────────────────

@app.route('/api/lorem/generate', methods=['POST'])
def api_lorem_generate():
    data = request.get_json()
    count = data.get('count', 5)
    unit = data.get('unit', 'paragraphs')
    try:
        result = generate_lorem(count, unit)
        return jsonify({'success': True, 'result': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


# ─── API: QR Generator ────────────────────────────────────────────────────────

@app.route('/api/qr/generate', methods=['POST'])
def api_qr_generate():
    data = request.get_json()
    text = data.get('text', '')
    size = data.get('size', 10)
    try:
        result = generate_qr(text, size)
        return jsonify({'success': True, 'result': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


# ─── Health Check ──────────────────────────────────────────────────────────────

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'name': 'CodeForge', 'version': '1.0.0'})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
