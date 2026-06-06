<p align="center">
  <img src="https://img.shields.io/badge/CodeForge-v1.0-6366f1?style=for-the-badge" alt="CodeForge">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-3.x-000000?style=flat-square&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/Status-Active-success?style=flat-square" alt="Status">
</p>

<h1 align="center">⚡ CodeForge — All-in-One Developer Tools Suite</h1>

<p align="center"><strong>A powerful, web-based developer tools platform that actually runs.</strong></p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#demo">Demo</a> •
  <a href="#installation">Installation</a> •
  <a href="#tools">Tools</a> •
  <a href="#api">API</a> •
  <a href="#license">License</a>
</p>

---

## ✨ Features

- 🎨 **Modern Dark Theme** — Beautiful UI with light/dark mode toggle
- ⚡ **10 Built-in Tools** — Everything a developer needs in one place
- 🔌 **REST API** — Every tool is accessible via API endpoints
- 📱 **Responsive** — Works on desktop, tablet, and mobile
- 🚀 **Zero Config** — Just install and run

## 🛠️ Tools

| # | Tool | Description |
|---|------|-------------|
| 1 | 🗂️ **JSON Formatter** | Format, minify, and validate JSON with syntax highlighting |
| 2 | 🔍 **Regex Tester** | Test regex patterns with real-time match highlighting |
| 3 | 🔐 **Hash Generator** | Generate MD5, SHA1, SHA256, SHA512, bcrypt hashes |
| 4 | 🔄 **Base64 Codec** | Encode and decode Base64 strings |
| 5 | 🔗 **URL Codec** | URL encode and decode strings |
| 6 | 🎫 **JWT Decoder** | Decode JWT tokens (header, payload, signature) |
| 7 | 📊 **Diff Checker** | Compare two texts with inline diff highlighting |
| 8 | 🎨 **Color Converter** | Convert between HEX, RGB, and HSL color formats |
| 9 | 📝 **Lorem Ipsum Generator** | Generate placeholder text (words, sentences, paragraphs) |
| 10 | 📱 **QR Code Generator** | Generate QR codes from any text or URL |

## 🚀 Installation

### Prerequisites
- Python 3.10+
- pip

### Quick Start

```bash
# Clone the repository
git clone https://github.com/mayank-dev-15/codeforge.git
cd codeforge

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

Open your browser and navigate to `http://localhost:5000`

### Docker (optional)

```bash
docker build -t codeforge .
docker run -p 5000:5000 codeforge
```

## 📡 API Endpoints

All tools are accessible via REST API:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/json/format` | POST | Format/minify JSON |
| `/api/json/validate` | POST | Validate JSON |
| `/api/regex/test` | POST | Test regex pattern |
| `/api/hash/generate` | POST | Generate hashes |
| `/api/base64/encode` | POST | Base64 encode |
| `/api/base64/decode` | POST | Base64 decode |
| `/api/url/encode` | POST | URL encode |
| `/api/url/decode` | POST | URL decode |
| `/api/jwt/decode` | POST | Decode JWT token |
| `/api/diff/check` | POST | Compare two texts |
| `/api/color/convert` | POST | Convert color formats |
| `/api/lorem/generate` | POST | Generate lorem ipsum |
| `/api/qr/generate` | POST | Generate QR code |
| `/api/health` | GET | Health check |

### Example API Usage

```bash
# Format JSON
curl -X POST http://localhost:5000/api/json/format \
  -H "Content-Type: application/json" \
  -d '{"text": "{\"name\":\"CodeForge\"}", "indent": 2}'

# Generate hash
curl -X POST http://localhost:5000/api/hash/generate \
  -H "Content-Type: application/json" \
  -d '{"text": "hello world", "algorithms": ["md5", "sha256"]}'

# Decode JWT
curl -X POST http://localhost:5000/api/jwt/decode \
  -H "Content-Type: application/json" \
  -d '{"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."}'
```

## 🏗️ Project Structure

```
codeforge/
├── app.py                  # Flask application & API routes
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── LICENSE                # MIT License
├── .gitignore             # Git ignore rules
├── tools/                 # Tool modules
│   ├── __init__.py
│   ├── json_formatter.py
│   ├── regex_tester.py
│   ├── hash_generator.py
│   ├── base64_codec.py
│   ├── url_codec.py
│   ├── jwt_decoder.py
│   ├── diff_checker.py
│   ├── color_picker.py
│   ├── lorem_generator.py
│   └── qr_generator.py
├── templates/
│   └── index.html         # Single-page app
└── static/
    ├── style.css          # Dark theme styling
    └── app.js             # Frontend JavaScript
```

## ⌨️ Keyboard Shortcuts

- `Ctrl+Enter` — Run current tool

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<p align="center">
  Built with ❤️ by <a href="https://github.com/mayank-dev-15">Mayank Basena</a>
</p>
