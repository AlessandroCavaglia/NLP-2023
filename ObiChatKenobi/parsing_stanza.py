import stanza
#http://nlpviz.bpodgursky.com/
#https://cs.nyu.edu/~grishman/jet/guide/PennPOS.html
def main():
    nlp = stanza.Pipeline('en') # initialize English neural pipeline

    doc = nlp("I don't think that it's not 3") # run annotation over a sentence

    verb=None
    complement=None
    adverb=[]

    #print(doc.sentences[0])

    for elem in doc.sentences[0]._words:
        if(elem.lemma=="be"):
            verb=elem
    for elem in doc.sentences[0]._words:
        if(elem.head==verb.head and elem.xpos=="RB"):
            adverb.append(elem)
        if(elem.id==verb.head):
            complement=elem


    print("Verb:",verb)
    print("Complement:",complement)
    print("Adverb:",adverb)


    print("-----------------------")
    print(doc.sentences[0]._constituency)

    #print(doc.sentences[0]._dependencies)


if __name__=="__main__":
    main()