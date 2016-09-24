import re
import nltk
import os
import sys
import readline
import json
from pprint import pprint
from Train import *
from xml.dom.minidom import parseString

reload(sys)
sys.setdefaultencoding("utf-8")

sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
word_tokenizer = nltk.tokenize.TreebankWordTokenizer()

default_tagger = nltk.UnigramTagger(uni_words, backoff=nltk.data.load(nltk.tag._POS_TAGGER))
tagger = nltk.BigramTagger(bi_words, backoff=default_tagger)

grammar = r"""
        NP: {<NNP>+}
        QP: {<W.*>}
        SUB:{<DEP>+|<CLUB>+}
"""
parser = nltk.RegexpParser(grammar)

print "Hi My name is Arya, How can I help you??"
reply = raw_input()
chunked = parser.parse(tagger.tag(word_tokenizer.tokenize(reply)))
#print chunked

def removeStop(sent):
    stop = [u'all', u'just', u'being', u'over', u'both', u'through', u'yourselves',
     u'its', u'before', u'o', u'hadn', u'herself', u'll', u'had', u'should', u'to',
     u'only', u'won', u'under', u'ours', u'has', u'do', u'them', u'his', u'very',
      u'they', u'not', u'during', u'now', u'him', u'nor', u'd', u'did', u'didn',
      u'this', u'she', u'each', u'further', u'where', u'few', u'because', u'doing',
       u'some', u'hasn', u'are', u'our', u'ourselves', u'out', u'for', u'while',
       u're', u'does', u'above', u'between', u'mustn', u't', u'be', u'we', u'who', u'were',
       u'here', u'shouldn', u'hers', u'by', u'on', u'about', u'couldn', u'of',
       u'against', u's', u'isn', u'or', u'own', u'into', u'yourself', u'down', u'mightn',
        u'wasn', u'your', u'from', u'her', u'their', u'aren', u'there', u'been',
         u'too', u'wouldn', u'themselves', u'weren', u'was', u'until', u'more', u'himself',
          u'that', u'but', u'don', u'with', u'than', u'those', u'he', u'me', u'myself',
           u'ma', u'these', u'up', u'will', u'below', u'ain', u'can', u'theirs', u'my',
           u'and', u've', u'then', u'is', u'am', u'it', u'doesn', u'an', u'as', u'itself',
            u'at', u'have', u'in', u'any', u'if', u'again', u'no', u'same', u'other',
             u'you', u'shan', u'needn', u'haven', u'after', u'most', u'such', u'a', u'off',
              u'i', u'm', u'yours', u'so', u'y', u'the', u'having', u'once']
    filtered_words = [w for w in sent.split() if not w in stop]
    #print filtered_words
    return filtered_words

def getName(chunked):
    try:
        for subtree in chunked.subtrees(filter=lambda t: t.label() == 'NP'):
            PNoun = " ".join(str(tup[0]) for tup in subtree.leaves())
        return PNoun
    except:
        print "Sorry Didn't get your name!!"
        name = raw_input()
        return getName(parser.parse(tagger.tag(word_tokenizer.tokenize(name))))
Name_User = getName(chunked)

def getQuestion(chunked):
    try:
        for subtree in chunked.subtrees(filter=lambda t: t.label() == 'QP'):
            Question = " ".join(str(tup[0]) for tup in subtree.leaves())
        return Question
    except:
        print "You didn't ask a Question!! Ask me something"
        q = raw_input()
        return getQuestion(parser.parse(tagger.tag(word_tokenizer.tokenize(q))))

def getKeywords(arg1,arg2,sent):
    q = []
    for w in sent:
        if w not in arg1 and w not in arg2:
            q.append(w)
    return q

def getSubject(chunked):
    try:
        for subtree in chunked.subtrees(filter=lambda t: t.label() == 'SUB'):
            Question = " ".join(str(tup[0]) for tup in subtree.leaves())
        return Question
    except:
        print "I don't understand:(\nWhat specifically are you talking about??"
        q = raw_input()
        return q

def parseJson(qType,Subject,keywords):
    with open('KnowledgeBase.json') as data_file:
        KB_JSON = json.load(data_file)
    #print KB_JSON
    if qType.lower() not in KB_JSON:
        raise ValueError("Ask a question!!!")
    X = KB_JSON[qType.lower()]
    #print X
    should_restart = True
    while should_restart:
        should_restart = False
        for i in keywords:
            try:
                if i.lower() in X:
                    X = X[i.lower()]
                    should_restart = True
                    break
            except:
                break
    try:
        print X['default']
    except:
        print X


Current_Context = "NITK"
print "Hi " + Name_User + ", How can I be of assistance?"
while(True):
    try:
        question = raw_input(">> ")
        if question.upper() == "QUIT":
            break
        try:
            question = question.replace("this",Current_Context)
        except:
            pass
        question = removeStop(question)
        #print (tagger.tag(question))
        chunked = parser.parse(tagger.tag(question))
        qType = getQuestion(chunked)
        subject = getSubject(chunked)
        Current_Context = subject
        keywords = getKeywords(qType, subject,question)
        parseJson(qType,subject,keywords)
    except:
        continue
