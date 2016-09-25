from engine import *

print "Hi My name is Arya, What's yours?"
reply = raw_input()
chunked = parser.parse(tagger.tag(word_tokenizer.tokenize(reply)))
#print chunked

chat_log = open("Chatlogs/"+Name_User+"_"+str(datetime.datetime.now()))

Current_Context = "ACM"
print "Hi " + Name_User + ", How can I be of assistance?"

while(True):
    try:
        question = raw_input(">> ")
        chat_log.write("QUESTION: " + question + "\n")

        if question.upper() == "QUIT":
            chat_log.close()
            break
        try:
            question = question.replace("this",Current_Context)
        except:
            pass
        print (tagger.tag(word_tokenizer.tokenize(question)))
        qType = getQuestion(question)

        chunked = parser.parse(tagger.tag(word_tokenizer.tokenize(question)))
        subject = getSubject(chunked)
        Current_Context = subject

        question = removeStop(question)
        keywords = getKeywords(qType, subject,question)

        answer = parseJson(qType,subject,keywords)
        print answer
        chat_log.write("ANSWER: " + answer + "\n")

    except Exception, e:
        chat_log.write("ERROR: " + str(e) + "\n")
        continue