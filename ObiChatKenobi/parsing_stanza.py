import stanza


# http://nlpviz.bpodgursky.com/
# https://cs.nyu.edu/~grishman/jet/guide/PennPOS.html
def main_single_complement():
    nlp = stanza.Pipeline('en')  # initialize English neural pipeline

    doc = nlp("I don't think that it's not 3")  # run annotation over a sentence

    verb = None
    complement = None
    adverb = []

    # print(doc.sentences[0])

    for elem in doc.sentences[0]._words:
        if (elem.lemma == "be"):
            verb = elem
    for elem in doc.sentences[0]._words:
        if (elem.head == verb.head and elem.xpos == "RB"):
            adverb.append(elem)
        if (elem.id == verb.head):
            complement = elem

    print("Verb:", verb)
    print("Complement:", complement)
    print("Adverb:", adverb)


def get_leaf_nodes(self):
    leafs = []

    def _get_leaf_nodes(node, parent):
        if node is not None:
            node.parent = parent
            if len(node.children) == 0:
                leafs.append(node)
            for n in node.children:
                _get_leaf_nodes(n, node)

    _get_leaf_nodes(self.children[0], None)
    return leafs


def findComplement(node):
    foundNode=None
    if(node.label=="NP"):
        foundNode= node
    else:
        index=0
        while(index<len(node.children) and foundNode==None):
            foundNode=findComplement(node.children[index])
            index=index+1

    return foundNode

def main_multiple_complement():
    nlp = stanza.Pipeline('en')  # initialize English neural pipeline

    doc = nlp("I think that it's not 3 or 5")  # run annotation over a sentence

    verb = None
    complement = None
    adverb = []

    # print(doc.sentences[0])
    for elem in doc.sentences[0]._words:
        if (elem.lemma == "be"):
            verb = elem
    for elem in doc.sentences[0]._words:
        if (elem.head == verb.head):
            print("--brother  ", elem)
        if (elem.id == verb.head):
            complement = elem
    '''for elem in doc.sentences[0]._words:
        if (elem.head == complement.head):
            print("--parent brother  ",elem)'''


def main_tree():
    nlp = stanza.Pipeline('en')  # initialize English neural pipeline

    doc = nlp("I think that it is not 3 or 5")  # run annotation over a sentence

    sent = doc._sentences[0]._constituency

    verb=None
    complement=None
    for node in get_leaf_nodes(sent):
        if(node.label=="is"):
            verb=node
            exploreNode=verb
            while(exploreNode.label!="VP"):
                exploreNode=exploreNode.parent
            complement=findComplement(exploreNode)

    print(verb)
    print(complement)



if __name__ == "__main__":
    main_tree()
