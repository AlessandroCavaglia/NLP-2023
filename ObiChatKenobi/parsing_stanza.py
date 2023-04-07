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


def extract_lemma(phrase, dictionary):
    verbs = []
    visited_node = []
    complement = None
    adverb = []
    for elem in phrase.sentences[0]._words:
        if (elem.lemma in dictionary):
            verbs.append(elem)
    '''
    for verb in verbs:
        for elem in phrase.sentences[0]._words:
            if verb.id not in visited_node :
                visited_node.append(verb.id)
                if (elem.head == verb.head and elem.xpos == "RB"):
                    adverb.append(elem)
                if (elem.id == verb.head):
                    complement = elem
    '''
    return verbs


def elaborateModifier(modifiers):
    result = None
    for modifier in modifiers:
        if modifier == "not" or modifier == "n't":
            result = "!"
    return result


def elaborateComplement(root):
    complements = []
    for child in root.children:
        if (len(child.children) == 0):
            if (child.label == "or"):
                complements.append("|")
            elif (child.label == "not"):
                complements.append("!")
            elif (child.label == "and" or child.label == ","):
                complements.append("&")
            else:
                complements.append(child.label)
        else:
            complements.extend(elaborateComplement(child))
    return complements


def mergeComplements(complements, modifier):
    for i in range(len(complements)):
        if (complements[i] == "!"):
            if (complements[i + 1] == "!"):
                complements[i + 1] = ""
            else:
                complements[i + 1] = "!" + complements[i + 1]
            complements[i] = ""
    while (complements.count("") > 0):
        complements.remove("")
    if (modifier == "!"):
        for i,complement in enumerate(complements):
            if (complement.startswith("!")):
                complements[i] = complement[1:]
            else:
                if (complement == "&"):
                    complements[i] = "|"
                elif (complement == "|"):
                    complements[i] = "&"
                else:
                    complements[i] = "!" + complement
    return complements


def build_merged_tree():
    nlp = stanza.Pipeline('en')  # initialize English neural pipeline

    # doc = nlp("I think that it be not 3 or 5, it be 1 or 2, You must make 4 and 6")  # run annotation over a sentence
    doc = nlp("I think that it isn't Rome or Paris")  # run annotation over a sentence
    sent = doc._sentences[0]._constituency
    leaf_nodes = get_leaf_nodes(sent)

    # print(leaf_nodes)

    for verb in extract_lemma(doc, ["be", "make"]):
        current_verb = verb._text

        complementBlock = None
        complements = None
        modifierBlock = None
        modifier = None
        for node in leaf_nodes:
            if (node.label == current_verb):
                verb = node
                leaf_nodes.pop(leaf_nodes.index(node))
                exploreNode = verb
                while (exploreNode.label != "VP"):
                    exploreNode = exploreNode.parent
                complementBlock = findComplement(exploreNode)
                modifierBlock = findModifiers(exploreNode)
                modifier = elaborateModifier(modifierBlock)
                complements = mergeComplements(elaborateComplement(complementBlock), modifier)

                break

        print(verb)
        print(complementBlock)
        print(complements)
        print(modifierBlock)


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
    foundNode = None
    if (node.label == "NP"):
        foundNode = node
    else:
        index = 0
        while (index < len(node.children) and foundNode == None):
            foundNode = findComplement(node.children[index])
            index = index + 1

    return foundNode


def findModifiers(node):
    foundNodes = []
    if (node.label == "RB"):
        foundNodes.append(node.children[0].label)
    else:
        index = 0
        for child in node.children:
            if (child.label == "RB"):
                foundNodes.append(child.children[0].label)
    return foundNodes


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

    doc = nlp("I think that it is not 3 or 5 or 7")  # run annotation over a sentence

    sent = doc._sentences[0]._constituency

    verb = None
    complement = None
    modifier = None
    for node in get_leaf_nodes(sent):
        if (node.label == "is"):
            verb = node
            exploreNode = verb
            while (exploreNode.label != "VP"):
                exploreNode = exploreNode.parent
            complement = findComplement(exploreNode)
            modifier = findModifiers(exploreNode)

    print(verb)
    print(complement)


if __name__ == "__main__":
    build_merged_tree()
