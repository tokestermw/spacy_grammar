from spacy.tokens import Doc, Span, Token
from spacy.matcher import PhraseMatcher

from .utils import load_grammar_file

PREFIX = 'g_'


# TODO: put into class (to keep descriptions, etc.)?
def parse_grammar_matchers(nlp):
    grammar_file = load_grammar_file(nlp.lang)
    matchers = []
    for category, rule in grammar_file.items():
        matcher = PhraseMatcher(nlp.vocab)
        for name, attributes in rule.items():
            grammar_patterns = map(nlp, attributes['patterns'])
            matcher.add(name, None, *grammar_patterns)
            Token.set_extension(PREFIX + name, default=False)
        matchers.append(matcher)
    return matchers


class Grammar(object):

    def __init__(self, nlp, merge_spans=False):

        self.merge_spans = merge_spans
        self.matchers = parse_grammar_matchers(nlp)

    def __call__(self, doc):

        matches = []
        for matcher in self.matchers:
            matches.extend(matcher(doc))

        spans = []  # keep spans here to merge them later
        for ent_id, start, end in matches:
            ent_name = doc.vocab[ent_id].text
            span = doc[start : end]
            for token in span:
                token._.set(PREFIX + ent_name, True)
            spans.append(span)
        if self.merge_spans:
            for span in spans:
                span.merge()
        return doc


if __name__ == '__main__':
    import spacy
    nlp = spacy.load('en_core_web_sm')
    grammar = Grammar(nlp)
    nlp.add_pipe(grammar)
    doc = nlp('We can elaborate this distinction as follow.')
    print([i._.g_as_follow_as_follows for i in doc])
    # [False, False, False, False, False, True, True, False]
