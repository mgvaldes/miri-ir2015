__author__ = 'gaby'

from codecs import decode
import re
from nltk.corpus import stopwords
# from pymongo import MongoClient


def insert_document_to_corpus(file_name, class_name, db):
    # conn = MongoClient()
    # db = conn.foo
    cached_stop_words = stopwords.words("english")

    with open(file_name) as f:
        text = []
        for line in f:
            for word in line.strip().split():
                if word not in cached_stop_words:
                    word = decode(word.strip(), 'latin2', 'ignore')
                    word = re.sub(r'[^a-zA-Z ]', r'', word)
                    text.append(word.lower())

        d = dict()
        d['content'] = text
        d['class'] = class_name
        db.corpus.insert(d)