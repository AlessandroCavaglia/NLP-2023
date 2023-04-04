import spacy_udpipe
def main():
    text = "I think the answer isn't pizza"
    nlp = spacy_udpipe.load("en")

    doc = nlp(text)
    for token in doc:
        if(token.pos_=="AUX"):
            print(token.text)
            for token in token.ancestors:
                    print("Par - ",token.text, token.lemma_, token.pos_, token.dep_)
                    for token in token.ancestors:
                        print("Par Par - ", token.text, token.lemma_, token.pos_, token.dep_)

            for token in token.children:
                print("Child - ", token.text, token.lemma_, token.pos_, token.dep_)





if __name__=="__main__":
    main()