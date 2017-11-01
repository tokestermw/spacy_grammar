from spacy.tokens import Doc, Span, Token
from spacy.matcher import Matcher, PhraseMatcher

from .utils import load_grammar_file

PREFIX = 'g_'

STRING_TYPE = 'string'
SPACY_TYPE = 'spacy'

SPACY_ATTRS = {
    'ORTH',
    'LOWER', 'UPPER',
    'IS_ALPHA', 'IS_ASCII', 'IS_DIGIT',
    'IS_LOWER', 'IS_UPPER', 'IS_TITLE',
    'IS_PUNCT', 'IS_SPACE', 'IS_STOP',
    'LIKE_NUM', 'LIKE_URL', 'LIKE_EMAIL',
    'POS','TAG', 'DEP', 'LEMMA', 'SHAPE',
}


class PatternException(Exception):
    pass


class AttributeException(Exception):
    pass


# TODO: slow?
def _check_pattern_type(pattern):
    if isinstance(pattern, str):
        return STRING_TYPE
    elif isinstance(pattern, list):
        for token in pattern:
            if not isinstance(token, dict):
                raise PatternException(type(token))
            for key in token.keys():
                if key not in SPACY_ATTRS:
                    raise AttributeException(key)
        return SPACY_TYPE
    else:
        raise PatternException(type(pattern))


# TODO: put into class (to keep descriptions, etc.)?
def parse_grammar_matcher(nlp):
    grammar_file = load_grammar_file(nlp.lang)

    matcher = Matcher(nlp.vocab)
    phrase_matcher = PhraseMatcher(nlp.vocab)

    for category, rule in grammar_file.items():
        for name, attributes in rule.items():
            # grammar_patterns = map(nlp, attributes['patterns'])
            for pattern in attributes['patterns']:
                pattern_type = _check_pattern_type(pattern)
                if pattern_type == STRING_TYPE:
                    phrase_matcher.add(name, None, nlp(pattern))
                elif pattern_type == SPACY_TYPE:
                    matcher.add(name, None, pattern)
            Token.set_extension(PREFIX + name, default=False)

    return matcher, phrase_matcher
