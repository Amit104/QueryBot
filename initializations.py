import re
import nltk
import os
import sys
import readline
import json
from pprint import pprint
from Train import *
import datetime
from xml.dom.minidom import parseString
import random

reload(sys)
sys.setdefaultencoding("utf-8")

sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
word_tokenizer = nltk.tokenize.TreebankWordTokenizer()

default_tagger = nltk.UnigramTagger(uni_words, backoff=nltk.data.load(nltk.tag._POS_TAGGER))
tagger = nltk.BigramTagger(bi_words, backoff=default_tagger)

qWords = ["what","who","why","when","how","whom","which","whenever","is","are","do","does","did","give","tell"]

grammar = r"""
        NP: {<NNP>+}
        QP: {<W.*>}
        SUB:{<DEP>+|<CLUB>+}
"""
parser = nltk.RegexpParser(grammar)
