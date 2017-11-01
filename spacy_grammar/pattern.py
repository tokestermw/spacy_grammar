from spacy.tokens import Doc, Span, Token
from spacy.matcher import PhraseMatcher

from .utils import load_grammar_file

PREFIX = 'g_'


# TODO: put into class (to keep descriptions, etc.)?
def parse_grammar_matcher(nlp):
    grammar_file = load_grammar_file(nlp.lang)
    matcher = PhraseMatcher(nlp.vocab)
    for category, rule in grammar_file.items():
        matcher = PhraseMatcher(nlp.vocab)
        for name, attributes in rule.items():
            grammar_patterns = map(nlp, attributes['patterns'])
            matcher.add(name, None, *grammar_patterns)
            Token.set_extension(PREFIX + name, default=False)
    return matcher
