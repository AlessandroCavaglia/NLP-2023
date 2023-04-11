import stanza


# http://nlpviz.bpodgursky.com/
# https://cs.nyu.edu/~grishman/jet/guide/PennPOS.html

def preProcess(phrase):
    phrase=phrase.capitalize()
    return phrase

def extract_lemma(phrase, dictionary):
    """ Extracts the test verb  of the phrase given a set of possible lemmas """
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
    """ Groups together some modifiers of the verb to make it easier later to work """
    result = []
    for modifier in modifiers:
        if modifier == "not" or modifier == "n't":
            result.append("!")
        else:
            result.append(modifier)
    return result


def elaborateComplement(root):
    """ Extracts child elements from the complement sub-tree """
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


def mergeComplements(complements, modifiers):
    """ Applies logic rules based on the modifiers to the complements """
    if(len(complements)==0):
        return []
    #Unisco i complementi
    index=0
    while(index<len(complements)-1):
        #Se la cella attuale è una parola e se la cella successiva è una parola
        if(complements[index]!="!" and complements[index]!="&" and complements[index]!="|") and (complements[index+1]!="!" and complements[index+1]!="&" and complements[index+1]!="|"):
            #Merge delle parole
            complements[index]=complements[index]+" "+complements[index+1]
            complements.remove(complements[index+1])
            #Resetto la ricerca
            index=0
        else:
            index=index+1

    #Applico le negazioni locali
    for i in range(len(complements)):
        if (complements[i] == "!"):
            if (complements[i + 1] == "!"):
                complements[i + 1] = ""
            else:
                complements[i + 1] = "!" + complements[i + 1]
            complements[i] = ""
    while (complements.count("") > 0):
        complements.remove("")
    # Applico le negazioni globali
    if ("!" in modifiers):
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


def get_leaf_nodes(self):
    """ Extract all the leaf nodes from the tree and adds the parent reference in each node """
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
    """ Extracts the subtree relative to the complement of the verb"""
    foundNode = None
    if (node.label == "NP" or node.label=="ADJP"):
        foundNode = node
    else:
        index = 0
        while (index < len(node.children) and foundNode == None):
            foundNode = findComplement(node.children[index])
            index = index + 1

    return foundNode


def findModifiers(node):
    """ Extracts the modifiers of the verb """
    foundNodes = []
    if(node.parent.label=="VP"):
        foundNodes=findModifiers(node.parent)
    if (node.label == "RB" or node.label == "MD" or node.label=="ADVP"):
        foundNodes.append(node.children[0].label)
    else:
        for child in node.children:
            if (child.label == "RB" or child.label == "MD" or node.label=="ADVP"):
                foundNodes.append(child.children[0].label)
    return foundNodes


def understand_answer(phrase,suggested_verbs):
    nlp = stanza.Pipeline('en')  # initialize English neural pipeline
    #doc = nlp("I think that it be not 3 or 5, it be 1 or 2, You must make 4 and 6")  # run annotation over a sentence
    doc = nlp(preProcess(phrase))  # run annotation over a sentence
    sent = doc._sentences[0]._constituency
    leaf_nodes = get_leaf_nodes(sent)

    complements = []
    modifiers = []
    for verb in extract_lemma(doc, suggested_verbs):
        complementBlock = None
        modifierBlock = None
        local_modifiers = None
        local_complements = None
        current_verb = verb._text
        for node in leaf_nodes:
            try:
                if (node.label == current_verb):
                    verb = node
                    leaf_nodes.pop(leaf_nodes.index(node))
                    exploreNode = verb
                    while (exploreNode.label != "VP"):
                        exploreNode = exploreNode.parent
                    complementBlock = findComplement(exploreNode)
                    modifierBlock = findModifiers(exploreNode)
                    local_modifiers = elaborateModifier(modifierBlock)
                    if(complementBlock!=None):
                        local_complements = elaborateComplement(complementBlock)
                    else:
                        local_complements=[]
                    local_complements = mergeComplements(local_complements, local_modifiers)
                    break
            except:
                local_modifiers=[None]
                local_complements=[None]
                print("Error")



        print(local_complements)
        complements.append(local_complements)
        print(local_modifiers)
        modifiers.append(local_modifiers)

    print(complements)
    print(modifiers)


if __name__ == "__main__":
    understand_answer("Rome",["be"])

    '''questions = ["How old are you?","In which country does Rome reside?","Can a priest get married?"]
    for quest in questions:
        print(quest)
        ans=input()
        understand_answer(ans,["be","reside","can","can't"])'''
