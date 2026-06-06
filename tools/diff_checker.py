"""Text Diff Checker."""


def check_diff(text1, text2):
    """Compare two texts and return diff information."""
    lines1 = text1.splitlines(keepends=True)
    lines2 = text2.splitlines(keepends=True)

    # Ensure lines end with newline for cleaner diff
    if lines1 and not lines1[-1].endswith('\n'):
        lines1[-1] += '\n'
    if lines2 and not lines2[-1].endswith('\n'):
        lines2[-1] += '\n'

    diff = list(__import__('difflib').unified_diff(
        lines1, lines2,
        fromfile='Text 1', tofile='Text 2',
        lineterm=''
    ))

    # Also compute inline diff for each changed line
    sm = __import__('difflib').SequenceMatcher(None, text1, text2)
    opcodes = sm.get_opcodes()

    changes = []
    added = 0
    removed = 0
    modified = 0

    for tag, i1, i2, j1, j2 in opcodes:
        if tag == 'insert':
            changes.append({'type': 'add', 'text': text2[j1:j2]})
            added += 1
        elif tag == 'delete':
            changes.append({'type': 'remove', 'text': text1[i1:i2]})
            removed += 1
        elif tag == 'replace':
            changes.append({'type': 'remove', 'text': text1[i1:i2]})
            changes.append({'type': 'add', 'text': text2[j1:j2]})
            modified += 1

    # Build highlighted text
    highlighted = _build_highlighted_diff(text1, text2, opcodes)

    return {
        'unified_diff': '\n'.join(diff),
        'changes': changes,
        'stats': {
            'added': added,
            'removed': removed,
            'modified': modified,
        },
        'similarity': round(sm.ratio() * 100, 2),
        'highlighted': highlighted,
    }


def _build_highlighted_diff(text1, text2, opcodes):
    """Build HTML-highlighted diff."""
    result = []
    for tag, i1, i2, j1, j2 in opcodes:
        if tag == 'equal':
            result.append(_escape(text1[i1:i2]))
        elif tag == 'insert':
            result.append(f'<ins>{_escape(text2[j1:j2])}</ins>')
        elif tag == 'delete':
            result.append(f'<del>{_escape(text1[i1:i2])}</del>')
        elif tag == 'replace':
            result.append(f'<del>{_escape(text1[i1:i2])}</del>')
            result.append(f'<ins>{_escape(text2[j1:j2])}</ins>')
    return ''.join(result)


def _escape(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
