from initializations import *

def removeStop(sent):
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
Name_User = "Chetan"

def getQuestion(question):
    try:
        qWord = None
        part_q = filter(None, re.split("[,\-!?:.]+", question))
        for que in part_q:
            words = word_tokenizer.tokenize(que)
            if words[0].lower() in qWords:
                qWord = words[0].lower()
        if qWord:
            return qWord
        else:
            raise Exception
    except:
        print "Please ask a question."
        return getQuestion(raw_input())


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
        return X['default']
    except:
        return X

def getRandom(list):
    return random.choice(list)

def reply(question):
    try:
        if question.upper() == "QUIT":
            chat_log.close()
            exit(0)
        try:
            question = question.replace("this",Current_Context)
        except:
            pass
        #print question
        #print (tagger.tag(word_tokenizer.tokenize(question)))
        qType = getQuestion(question)

        chunked = parser.parse(tagger.tag(word_tokenizer.tokenize(question)))
        subject = getSubject(chunked)
        Current_Context = subject

        question = removeStop(question)
        keywords = getKeywords(qType, subject,question)

        answer = parseJson(qType,subject,keywords)
        return answer
        

    except Exception, e:
        pass


