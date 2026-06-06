"""Lorem Ipsum Generator."""

import random

LOREM_WORDS = [
    "lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing", "elit",
    "sed", "do", "eiusmod", "tempor", "incididunt", "ut", "labore", "et", "dolore",
    "magna", "aliqua", "enim", "ad", "minim", "veniam", "quis", "nostrud",
    "exercitation", "ullamco", "laboris", "nisi", "aliquip", "ex", "ea", "commodo",
    "consequat", "duis", "aute", "irure", "in", "reprehenderit", "voluptate",
    "velit", "esse", "cillum", "fugiat", "nulla", "pariatur", "excepteur", "sint",
    "occaecat", "cupidatat", "non", "proident", "sunt", "culpa", "qui", "officia",
    "deserunt", "mollit", "anim", "id", "est", "laborum", "perspiciatis", "unde",
    "omnis", "iste", "natus", "error", "voluptatem", "accusantium", "doloremque",
    "laudantium", "totam", "rem", "aperiam", "eaque", "ipsa", "quae", "ab", "illo",
    "inventore", "veritatis", "quasi", "architecto", "beatae", "vitae", "dicta",
    "explicabo", "nemo", "ipsam", "quia", "voluptas", "aspernatur", "aut", "odit",
    "fugit", "consequuntur", "magni", "dolores", "eos", "ratione", "sequi",
    "nesciunt", "neque", "porro", "quisquam", "nihil", "impedit", "quo", "minus",
    "placeat", "facere", "possimus", "praesentium", "nam", "libero", "cum",
    "soluta", "nobis", "eligendi", "optio", "cumque", "impedit", "quod", "maxime",
]

SENTENCE_TEMPLATES = [
    "{word1} {word2} {word3} {word4} {word5}.",
    "{word1} {word2} {word3} {word4} {word5}, {word6} {word7} {word8}.",
    "{word1} {word2} {word3}, {word4} {word5} {word6} {word7} {word8} {word9}.",
    "{word1} {word2} {word3} {word4}, {word5} {word6} {word7}.",
    "{word1} {word2} {word3} {word4} {word5} {word6}, {word7} {word8}.",
]


def generate_lorem(count=5, unit='paragraphs'):
    """Generate lorem ipsum text."""
    if unit == 'words':
        return _generate_words(count)
    elif unit == 'sentences':
        return _generate_sentences(count)
    else:
        return _generate_paragraphs(count)


def _generate_words(count):
    words = [random.choice(LOREM_WORDS) for _ in range(count)]
    return ' '.join(words)


def _generate_sentences(count):
    sentences = []
    for _ in range(count):
        template = random.choice(SENTENCE_TEMPLATES)
        num_words = template.count('{')
        words = {f'word{i+1}': random.choice(LOREM_WORDS) for i in range(num_words)}
        sentence = template.format(**words)
        # Capitalize first letter
        sentence = sentence[0].upper() + sentence[1:]
        sentences.append(sentence)
    return ' '.join(sentences)


def _generate_paragraphs(count):
    paragraphs = []
    for _ in range(count):
        num_sentences = random.randint(4, 8)
        paragraphs.append(_generate_sentences(num_sentences))
    return '\n\n'.join(paragraphs)
