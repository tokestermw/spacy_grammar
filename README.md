## spacy_grammar: rule-based grammar detection for spaCy

This packages uses the [spaCy 2.0 alpha](https://alpha.spacy.io/usage/v2)
which provide support for adding custom attributes to `Doc`, `Span`, and
`Token` objects. It also leverages the [Matcher API](https://spacy.io/docs/usage/rule-based-matching)
in spaCy to quickly match on spaCy tokens not dissimilar to regex. It 
reads a `grammar.yml` file to load up custom patterns and returns the
results inside `Doc`, `Span`, and `Token`.

It is extensible through adding rules to `grammar.yml` (though currently 
only the simple string matching is implemented).

```
doc = nlp('I can haz cheeseburger.')
doc._.has_grammar_error  # True
```

A lot of thanks to [spacymoji](https://github.com/ines/spacymoji) and
[languagetool](https://www.languagetool.org) for inspiration.

## Install

This package uses Python 3.6.

```
python3.6 -m venv .
source bin/activate
pip install -r requirements.txt
```



The module uses the [`pipenv`](https://github.com/kennethreitz/pipenv) package
to handle dependencies. Once you install `pipenv`, you go to the root directory
and run:

```
pipenv install
```

and it will read the `Pipfile` to build the environment. To run the
virtualenv, simply:

```
pipenv shell
```

Run `exit` to exit out of the environment.

You will also need to install a spaCy model by:

```
python -m spacy download en_core_web_sm
```

## Usage

From the root directory, you can check to see if the package is working.

```
python -m spacy_grammar.grammar
```

This code checks to see if someone wrote `as follow` instead of `as follows`.

```
import spacy
nlp = spacy.load('en_core_web_sm')
grammar = Grammar(nlp)
nlp.add_pipe(grammar)
doc = nlp('We can elaborate this distinction as follow.')
print([i._.g_as_follow_as_follows for i in doc])
# [False, False, False, False, False, True, True, False]
```

## Adding rules

In `grammar.yml`, you can add rules following this template:

```
CATEGORY_NAME:
  RULE_NAME:
    description: 
    patterns: 
      - PATTERN_1
      - PATTERN_2
      ...
    corrections:
      - CORRECTION_1
      - CORRECTION_2
      ...
    examples: 
      - EXAMPLE_1
      - EXAMPLE_2
      ...

```