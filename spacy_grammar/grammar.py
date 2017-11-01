from itertools import chain

from .pattern import parse_grammar_matcher, PREFIX


class Grammar(object):

    def __init__(self, nlp):

        self.matcher, self.phrase_matcher = parse_grammar_matcher(nlp)

    def __call__(self, doc):

        matches = self.matcher(doc)
        phrase_matches = self.phrase_matcher(doc)

        # TODO: remove duplicates
        spans = []
        for ent_id, start, end in chain(matches, phrase_matches):
            ent_name = doc.vocab[ent_id].text
            span = doc[start : end]
            for token in span:
                token._.set(PREFIX + ent_name, True)
            spans.append(span)

        return doc


if __name__ == '__main__':
    import spacy
    nlp = spacy.load('en_core_web_sm')
    grammar = Grammar(nlp)
    nlp.add_pipe(grammar)
    doc = nlp('We can elaborate this distinction as follow.')
    print([i._.g_as_follow_as_follows for i in doc])
    # [False, False, False, False, False, True, True, False]
