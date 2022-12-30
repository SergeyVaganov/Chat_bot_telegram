import re
from . import dictionaries
from typing import Dict
from nltk.corpus import stopwords
import time
import importlib
from natasha import Doc, MorphVocab, Segmenter, NewsEmbedding, NewsMorphTagger
import nltk
nltk.download('stopwords')


dictionaries = importlib.reload(dictionaries)
segmenter = Segmenter()
morph_vocab = MorphVocab()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb) 


def lower_txt(input_txt: str) -> str:
    out_txt = input_txt.lower()
    return out_txt


def sub_txt(pattern: str, input_txt: str) -> str:
    out_txt = re.sub(pattern, ' ', input_txt)
    return out_txt


def replace_txt(replace_dict: Dict[str, str], input_txt: str) -> str:
    list_txt = []
    for word in input_txt.split():
        if word in replace_dict.keys():
            word = replace_dict[word]
        list_txt.append(word)
    out_txt = ' '.join(list_txt)
    return out_txt


def word_len(input_txt: str) -> str:
    return ' '.join([w for w in input_txt.split() if len(w) > 1])


def stop_wds(input_txt: str, leng: str, pos: bool = False) -> str:
    stop_words = stopwords.words(leng)
    if pos:
        out_txt = [word for word in input_txt.split() if not word.split(sep='_')[0] in stop_words]
    else:
        out_txt = [word for word in input_txt.split() if not word in stop_words]
    out_txt = ' '.join(out_txt)
    return out_txt


def natasha_lemmatize(input_txt: str, pos: bool = False) -> str:
    doc = Doc(input_txt)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    out_txt = ''
    for token in doc.tokens:
        token.lemmatize(morph_vocab)
        if pos:
            out_txt = [str(token.lemma) + '_' + str(token.pos) for token in doc.tokens]
        else:
            out_txt = [str(token.lemma) for token in doc.tokens]
        out_txt = ' '.join(out_txt)            
    return out_txt


def ru_preprocessing(input_txt: str, pos: bool = False) -> str:
    x = sub_txt(r'@[\w]*', input_txt)                       # удалим @user из всех твитов
    x = lower_txt(x)                                        # изменим регистр твитов
    x = replace_txt(dictionaries.ru_emoticon_dict, x)       # заменим эмотиконы
    x = sub_txt(r'[^\w\s]', x)                              # заменим пунктуацию на пробелы
    x = sub_txt(r'[^а-яёЁА-Я0-9]', x)                       # заменим спец. символы на пробелы
    x = sub_txt(r'[^а-яёЁА-Я]', x)                          # заменим числа на пробелы
    x = word_len(x)                                         # ограничим длинну слов
    x = natasha_lemmatize(x, pos)                           # лемматизируем слова
    x = stop_wds(x, 'russian', pos)                         # удалим стоп-слова
    return x
 

def en_preprocessing(input_txt: str) -> str:
    x = sub_txt(r'@[\w]*', input_txt)                   # удалим @user из всех твитов
    x = lower_txt(x)                                    # изменим регистр твитов
    x = replace_txt(dictionaries.apostrophe_dict, x)    # заменим сокращения с апострофами
    x = replace_txt(dictionaries.short_word_dict, x)    # заменим сокращения на их полные формы
    x = replace_txt(dictionaries.emoticon_dict, x)      # заменим эмотиконы
    x = sub_txt(r'[^\w\s]', x)                          # заменим пунктуацию на пробелы
    x = sub_txt(r'[^a-zA-Z0-9]', x)                     # заменим спец. символы на пробелы
    x = sub_txt(r'[^a-zA-Z]', x)                        # заменим числа на пробелы
    x = word_len(x)                                     # ограничим длинну слов
    x = stop_wds(x, 'english')                          # удалим стоп-слова
    return x


def new_awesome_function(a, b):
    print(a, 'start')
    time.sleep(1)
    print(a, 'end')
    return a + b

