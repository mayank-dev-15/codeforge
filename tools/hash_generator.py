"""Hash Generator supporting MD5, SHA1, SHA256, SHA512, and bcrypt."""

import hashlib
import bcrypt


def generate_hash(text, algorithms=None):
    """Generate hashes for the given text using specified algorithms."""
    if algorithms is None:
        algorithms = ['md5', 'sha1', 'sha256', 'sha512']

    if not text:
        raise ValueError("Input text is empty")

    text_bytes = text.encode('utf-8')
    results = {}

    for algo in algorithms:
        algo_lower = algo.lower().strip()
        if algo_lower == 'md5':
            results['md5'] = hashlib.md5(text_bytes).hexdigest()
        elif algo_lower == 'sha1':
            results['sha1'] = hashlib.sha1(text_bytes).hexdigest()
        elif algo_lower == 'sha256':
            results['sha256'] = hashlib.sha256(text_bytes).hexdigest()
        elif algo_lower == 'sha512':
            results['sha512'] = hashlib.sha512(text_bytes).hexdigest()
        elif algo_lower == 'bcrypt':
            salt = bcrypt.gensalt(rounds=12)
            results['bcrypt'] = bcrypt.hashpw(text_bytes, salt).decode('utf-8')
        else:
            results[algo_lower] = None

    return results
