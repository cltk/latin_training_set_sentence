"""Build a sentence tokenizer for a language. Latin below.
Some guidance available here: http://wiki.apertium.org/wiki/Sentence_segmenting
"""

from nltk.tokenize.punkt import PunktLanguageVars
from nltk.tokenize.punkt import PunktSentenceTokenizer
from nltk.tokenize.punkt import PunktTrainer
import os
import pickle

def train_from_file(training_file):
    #PunktLanguageVars
    language_punkt_vars = PunktLanguageVars
    language_punkt_vars.sent_end_chars=('.', '?', ':')
    #PunktTrainer
    language_punkt_vars.internal_punctuation=(',', ';')
    with open(training_file) as f:
        train_data = f.read()
    #build trainer
    trainer = PunktTrainer(train_data, language_punkt_vars)
    with open('latin.pickle', 'wb') as f:
        pickle.dump(trainer, f)

def tokenize_sentences(input_file):
    with open('latin.pickle', 'rb') as f:
        train_data = pickle.load(f)
    train_data.INCLUDE_ALL_COLLOCS = True
    train_data.INCLUDE_ABBREV_COLLOCS = True
    params = train_data.get_params()
    sbd = PunktSentenceTokenizer(params)
    with open(input_file) as f:
        to_be_tokenized = f.read()
    tokenenized_sentences = []
    for sentence in sbd.sentences_from_text(to_be_tokenized, realign_boundaries=True):
        tokenenized_sentences.append(sentence)
    #file_output_name = 'sentences_tokenized_' + input_file
    with open('tokenized_output.txt', 'w') as f:
        f.write(str(tokenenized_sentences))
    print(tokenenized_sentences)

def tokenize_sentences_string(sentences_string):
    '''
    default_cltk_data = '~/cltk_data'
    cltk_data = os.path.expanduser(default_cltk_data)
    compile_cltk_lat_sent_data = os.path.join(cltk_data, 'compiled', 'sentence_tokens_latin/')
    '''
    pickle_name = 'latin.pickle'
    #pickle_path = compile_cltk_lat_sent_data + pickle_name
    #print(pickle_path)
    with open(pickle_name, 'rb') as f:
        train_data = pickle.load(f)
    train_data.INCLUDE_ALL_COLLOCS = True
    train_data.INCLUDE_ABBREV_COLLOCS = True
    params = train_data.get_params()
    sbd = PunktSentenceTokenizer(params)
    tokenenized_sentences = []
    for sentence in sbd.sentences_from_text(sentences_string, realign_boundaries=True):
        tokenenized_sentences.append(sentence)
    return tokenenized_sentences


#for debugging
def main():
    training_file = 'training_sentences.txt'
    train_from_file(training_file)
    input_file = 'models/cat1.txt'
    tokenize_sentences(input_file)

if __name__ == '__main__':
    main()