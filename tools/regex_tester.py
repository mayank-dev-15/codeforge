"""Regex Tester with match highlighting."""

import re


def test_regex(pattern, text, flags_str=''):
    """Test a regex pattern against text. Returns match info."""
    if not pattern:
        raise ValueError("Pattern is empty")

    # Parse flags
    flags = 0
    flag_map = {
        'i': re.IGNORECASE,
        'm': re.MULTILINE,
        's': re.DOTALL,
        'x': re.VERBOSE,
        'a': re.ASCII,
        'l': re.LOCALE,
        'u': re.UNICODE,
    }
    for ch in flags_str.lower():
        if ch in flag_map:
            flags |= flag_map[ch]

    try:
        compiled = re.compile(pattern, flags)
    except re.error as e:
        raise ValueError(f"Invalid regex: {e}")

    matches = []
    for m in compiled.finditer(text):
        matches.append({
            'match': m.group(),
            'start': m.start(),
            'end': m.end(),
            'groups': list(m.groups()),
            'groupdict': m.groupdict(),
        })

    # Build highlighted text
    highlighted = _build_highlighted(text, matches)

    return {
        'matches': matches,
        'match_count': len(matches),
        'highlighted': highlighted,
        'groups': [m['groups'] for m in matches],
    }


def _build_highlighted(text, matches):
    """Build HTML-highlighted version of text with matches."""
    if not matches:
        return _escape_html(text)

    parts = []
    last_end = 0
    for i, m in enumerate(matches):
        start = m['start']
        end = m['end']
        if start > last_end:
            parts.append(_escape_html(text[last_end:start]))
        parts.append(f'<mark class="match-{i % 5}">')
        parts.append(_escape_html(text[start:end]))
        parts.append('</mark>')
        last_end = end
    if last_end < len(text):
        parts.append(_escape_html(text[last_end:]))

    return ''.join(parts)


def _escape_html(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
