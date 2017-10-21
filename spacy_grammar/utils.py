import os
import yaml

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


def load_grammar_file(lang='en'):
    path = os.path.join(CURRENT_DIR, lang, 'grammar.yml')
    with open(path, 'r') as f:
        grammar_file = yaml.safe_load(f)
    return grammar_file


if __name__ == '__main__':
    print(load_grammar_file())
