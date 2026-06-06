/* ═══════════════════════════════════════════════════════════════════════════
   CodeForge — Frontend JavaScript
   ═══════════════════════════════════════════════════════════════════════════ */

// ─── Navigation ───────────────────────────────────────────────────────────────

document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const tool = link.dataset.tool;
        switchTool(tool);
    });
});

function switchTool(toolId) {
    document.querySelectorAll('.tool-section').forEach(s => s.classList.remove('active'));
    document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
    document.getElementById('tool-' + toolId).classList.add('active');
    document.querySelector(`.nav-link[data-tool="${toolId}"]`).classList.add('active');
    window.location.hash = toolId;
}

// Load tool from hash
const hash = window.location.hash.slice(1);
if (hash && document.getElementById('tool-' + hash)) {
    switchTool(hash);
}

// ─── Theme Toggle ─────────────────────────────────────────────────────────────

const themeToggle = document.getElementById('theme-toggle');
const savedTheme = localStorage.getItem('codeforge-theme');
if (savedTheme === 'light') {
    document.documentElement.setAttribute('data-theme', 'light');
    themeToggle.textContent = '☀️';
}
themeToggle.addEventListener('click', () => {
    const isLight = document.documentElement.getAttribute('data-theme') === 'light';
    if (isLight) {
        document.documentElement.removeAttribute('data-theme');
        themeToggle.textContent = '🌙';
        localStorage.setItem('codeforge-theme', 'dark');
    } else {
        document.documentElement.setAttribute('data-theme', 'light');
        themeToggle.textContent = '☀️';
        localStorage.setItem('codeforge-theme', 'light');
    }
});

// ─── Toast ────────────────────────────────────────────────────────────────────

function showToast(msg, type = 'success') {
    const toast = document.getElementById('toast');
    toast.textContent = msg;
    toast.className = 'toast ' + type + ' show';
    setTimeout(() => toast.classList.remove('show'), 2500);
}

// ─── Clipboard Helpers ────────────────────────────────────────────────────────

function copyToClipboard(elementId) {
    const el = document.getElementById(elementId);
    const text = el ? (el.value || el.textContent) : '';
    if (!text) return;
    navigator.clipboard.writeText(text).then(() => {
        showToast('Copied to clipboard!');
    }).catch(() => {
        // Fallback
        const ta = document.createElement('textarea');
        ta.value = text;
        document.body.appendChild(ta);
        ta.select();
        document.execCommand('copy');
        document.body.removeChild(ta);
        showToast('Copied to clipboard!');
    });
}

async function pasteFromClipboard(elementId) {
    try {
        const text = await navigator.clipboard.readText();
        const el = document.getElementById(elementId);
        if (el) el.value = text;
    } catch {
        showToast('Clipboard access denied', 'error');
    }
}

function clearEditor(elementId) {
    const el = document.getElementById(elementId);
    if (el) el.value = '';
}

// ─── API Helper ───────────────────────────────────────────────────────────────

async function apiCall(endpoint, data) {
    const resp = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    });
    return resp.json();
}

// ─── JSON Formatter ───────────────────────────────────────────────────────────

async function formatJSON() {
    const text = document.getElementById('json-input').value;
    const indent = parseInt(document.getElementById('json-indent').value);
    const out = document.getElementById('json-output');
    const status = document.getElementById('json-status');
    try {
        const r = await apiCall('/api/json/format', { text, indent, action: 'format' });
        if (r.success) {
            out.textContent = r.result;
            status.textContent = '✓ Formatted successfully';
            status.className = 'status-bar success';
        } else {
            out.textContent = '';
            status.textContent = '✗ ' + r.error;
            status.className = 'status-bar error';
        }
    } catch (e) {
        status.textContent = '✗ Error: ' + e.message;
        status.className = 'status-bar error';
    }
}

async function minifyJSON() {
    const text = document.getElementById('json-input').value;
    const out = document.getElementById('json-output');
    const status = document.getElementById('json-status');
    try {
        const r = await apiCall('/api/json/format', { text, action: 'minify' });
        if (r.success) {
            out.textContent = r.result;
            status.textContent = '✓ Minified successfully';
            status.className = 'status-bar success';
        } else {
            out.textContent = '';
            status.textContent = '✗ ' + r.error;
            status.className = 'status-bar error';
        }
    } catch (e) {
        status.textContent = '✗ Error: ' + e.message;
        status.className = 'status-bar error';
    }
}

async function validateJSON() {
    const text = document.getElementById('json-input').value;
    const out = document.getElementById('json-output');
    const status = document.getElementById('json-status');
    try {
        const r = await apiCall('/api/json/validate', { text });
        out.textContent = '';
        if (r.valid) {
            status.textContent = '✓ Valid JSON';
            status.className = 'status-bar success';
        } else {
            status.textContent = '✗ Invalid JSON: ' + r.error;
            status.className = 'status-bar error';
        }
    } catch (e) {
        status.textContent = '✗ Error: ' + e.message;
        status.className = 'status-bar error';
    }
}

// ─── Regex Tester ─────────────────────────────────────────────────────────────

async function testRegex() {
    const pattern = document.getElementById('regex-pattern').value;
    const text = document.getElementById('regex-text').value;
    const flags = document.getElementById('regex-flags').value;
    const out = document.getElementById('regex-output');
    const count = document.getElementById('regex-count');
    const groups = document.getElementById('regex-groups');
    try {
        const r = await apiCall('/api/regex/test', { pattern, text, flags });
        if (r.success) {
            count.textContent = r.match_count;
            out.innerHTML = r.highlighted || '<span class="text-muted">No matches found</span>';
            // Show groups
            groups.innerHTML = '';
            if (r.matches && r.matches.length > 0) {
                r.matches.forEach((m, i) => {
                    const div = document.createElement('div');
                    div.className = 'regex-group-item';
                    let html = `<strong>Match ${i + 1}:</strong> "${m.match}" (pos ${m.start}-${m.end})`;
                    if (m.groups && m.groups.length > 0) {
                        html += `<br><strong>Groups:</strong> ${m.groups.map((g, j) => `$${j + 1}: "${g}"`).join(', ')}`;
                    }
                    if (m.groupdict && Object.keys(m.groupdict).length > 0) {
                        html += `<br><strong>Named:</strong> ${Object.entries(m.groupdict).map(([k, v]) => `${k}: "${v}"`).join(', ')}`;
                    }
                    div.innerHTML = html;
                    groups.appendChild(div);
                });
            }
        } else {
            out.innerHTML = '';
            count.textContent = '0';
            groups.innerHTML = '';
            showToast(r.error, 'error');
        }
    } catch (e) {
        showToast('Error: ' + e.message, 'error');
    }
}

// ─── Hash Generator ───────────────────────────────────────────────────────────

async function generateHash() {
    const text = document.getElementById('hash-input').value;
    const algorithms = [];
    if (document.getElementById('hash-md5').checked) algorithms.push('md5');
    if (document.getElementById('hash-sha1').checked) algorithms.push('sha1');
    if (document.getElementById('hash-sha256').checked) algorithms.push('sha256');
    if (document.getElementById('hash-sha512').checked) algorithms.push('sha512');
    if (document.getElementById('hash-bcrypt').checked) algorithms.push('bcrypt');
    const out = document.getElementById('hash-output');
    if (algorithms.length === 0) {
        showToast('Select at least one algorithm', 'error');
        return;
    }
    try {
        const r = await apiCall('/api/hash/generate', { text, algorithms });
        if (r.success) {
            out.innerHTML = '';
            const algoColors = { md5: '#58a6ff', sha1: '#3fb950', sha256: '#bc8cff', sha512: '#f778ba', bcrypt: '#d29922' };
            for (const [algo, hash] of Object.entries(r.hashes)) {
                if (!hash) continue;
                const item = document.createElement('div');
                item.className = 'hash-item';
                item.innerHTML = `
                    <span class="hash-algo" style="color:${algoColors[algo] || '#58a6ff'}">${algo}</span>
                    <div class="hash-value">
                        ${hash}
                        <button class="btn btn-sm hash-copy" onclick="navigator.clipboard.writeText('${hash.replace(/'/g, "\\'")}');showToast('Copied!')">📋</button>
                    </div>
                `;
                out.appendChild(item);
            }
        } else {
            showToast(r.error, 'error');
        }
    } catch (e) {
        showToast('Error: ' + e.message, 'error');
    }
}

// ─── Base64 Codec ─────────────────────────────────────────────────────────────

async function encodeBase64() {
    const text = document.getElementById('base64-input').value;
    const out = document.getElementById('base64-output');
    try {
        const r = await apiCall('/api/base64/encode', { text });
        out.textContent = r.success ? r.result : 'Error: ' + r.error;
    } catch (e) {
        out.textContent = 'Error: ' + e.message;
    }
}

async function decodeBase64() {
    const text = document.getElementById('base64-input').value;
    const out = document.getElementById('base64-output');
    try {
        const r = await apiCall('/api/base64/decode', { text });
        out.textContent = r.success ? r.result : 'Error: ' + r.error;
    } catch (e) {
        out.textContent = 'Error: ' + e.message;
    }
}

// ─── URL Codec ────────────────────────────────────────────────────────────────

async function encodeURL() {
    const text = document.getElementById('url-input').value;
    const out = document.getElementById('url-output');
    try {
        const r = await apiCall('/api/url/encode', { text });
        out.textContent = r.success ? r.result : 'Error: ' + r.error;
    } catch (e) {
        out.textContent = 'Error: ' + e.message;
    }
}

async function decodeURL() {
    const text = document.getElementById('url-input').value;
    const out = document.getElementById('url-output');
    try {
        const r = await apiCall('/api/url/decode', { text });
        out.textContent = r.success ? r.result : 'Error: ' + r.error;
    } catch (e) {
        out.textContent = 'Error: ' + e.message;
    }
}

// ─── JWT Decoder ──────────────────────────────────────────────────────────────

async function decodeJWT() {
    const token = document.getElementById('jwt-input').value;
    try {
        const r = await apiCall('/api/jwt/decode', { token });
        if (r.success) {
            document.getElementById('jwt-header').textContent = r.header_json;
            document.getElementById('jwt-payload').textContent = r.payload_json;
            document.getElementById('jwt-signature').textContent = r.signature;
        } else {
            showToast(r.error, 'error');
        }
    } catch (e) {
        showToast('Error: ' + e.message, 'error');
    }
}

// ─── Diff Checker ─────────────────────────────────────────────────────────────

async function checkDiff() {
    const text1 = document.getElementById('diff-text1').value;
    const text2 = document.getElementById('diff-text2').value;
    const out = document.getElementById('diff-output');
    const stats = document.getElementById('diff-stats');
    try {
        const r = await apiCall('/api/diff/check', { text1, text2 });
        if (r.success) {
            out.innerHTML = r.result.highlighted || '<span class="text-muted">No differences found</span>';
            const s = r.result.stats;
            stats.innerHTML = `
                <span class="diff-stat added">+ ${s.added} added</span>
                <span class="diff-stat removed">- ${s.removed} removed</span>
                <span class="diff-stat modified">~ ${s.modified} modified</span>
                <span class="diff-stat similarity">${r.result.similarity}% similar</span>
            `;
        } else {
            showToast(r.error, 'error');
        }
    } catch (e) {
        showToast('Error: ' + e.message, 'error');
    }
}

// ─── Color Converter ──────────────────────────────────────────────────────────

async function convertColor() {
    const color = document.getElementById('color-input').value;
    const preview = document.getElementById('color-preview');
    const results = document.getElementById('color-results');
    try {
        const r = await apiCall('/api/color/convert', { color });
        if (r.success) {
            preview.style.backgroundColor = r.hex;
            results.innerHTML = '';
            const items = [
                { label: 'HEX', value: r.hex },
                { label: 'RGB', value: r.rgb },
                { label: 'HSL', value: r.hsl },
            ];
            items.forEach(item => {
                const div = document.createElement('div');
                div.className = 'color-result-item';
                div.innerHTML = `
                    <span class="color-result-label">${item.label}</span>
                    <div class="color-result-value">
                        <span>${item.value}</span>
                        <button class="btn btn-sm" onclick="navigator.clipboard.writeText('${item.value}');showToast('Copied!')">📋</button>
                    </div>
                `;
                results.appendChild(div);
            });
        } else {
            showToast(r.error, 'error');
        }
    } catch (e) {
        showToast('Error: ' + e.message, 'error');
    }
}

// Sync color picker with text input
document.getElementById('color-picker').addEventListener('input', (e) => {
    document.getElementById('color-input').value = e.target.value;
    convertColor();
});

// ─── Lorem Generator ──────────────────────────────────────────────────────────

async function generateLorem() {
    const count = parseInt(document.getElementById('lorem-count').value) || 5;
    const unit = document.getElementById('lorem-unit').value;
    const out = document.getElementById('lorem-output');
    try {
        const r = await apiCall('/api/lorem/generate', { count, unit });
        out.textContent = r.success ? r.result : 'Error: ' + r.error;
    } catch (e) {
        out.textContent = 'Error: ' + e.message;
    }
}

// ─── QR Generator ─────────────────────────────────────────────────────────────

async function generateQR() {
    const text = document.getElementById('qr-input').value;
    const size = parseInt(document.getElementById('qr-size').value);
    const result = document.getElementById('qr-result');
    if (!text) {
        showToast('Enter text to encode', 'error');
        return;
    }
    try {
        const r = await apiCall('/api/qr/generate', { text, size });
        if (r.success) {
            result.innerHTML = `
                <img src="${r.result.base64}" alt="QR Code">
                <a href="${r.result.base64}" download="codeforge-qr.png" class="btn btn-secondary qr-download">📥 Download PNG</a>
            `;
        } else {
            showToast(r.error, 'error');
        }
    } catch (e) {
        showToast('Error: ' + e.message, 'error');
    }
}

// ─── Keyboard Shortcuts ───────────────────────────────────────────────────────

document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        // Run current tool
        const active = document.querySelector('.tool-section.active');
        if (!active) return;
        const toolId = active.id.replace('tool-', '');
        const fnMap = {
            json: formatJSON,
            regex: testRegex,
            hash: generateHash,
            base64: encodeBase64,
            url: encodeURL,
            jwt: decodeJWT,
            diff: checkDiff,
            color: convertColor,
            lorem: generateLorem,
            qr: generateQR,
        };
        if (fnMap[toolId]) fnMap[toolId]();
    }
});
