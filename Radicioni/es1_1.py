import csv
import math

from scipy.stats import pearsonr
from scipy.stats import spearmanr
from nltk.corpus import wordnet

WN_3_1_MAX_DEPTH=20

def read_csv(filename):
    dataset=[]
    with open(filename, 'r') as file:
        # Create a CSV reader object
        reader = csv.reader(file)
        for row in reader:
            row[2]=float(row[2])
            dataset.append(row+[None,None,None])
    return dataset

def normalize(value, min_val, max_val):
    return (value - min_val) / (max_val - min_val)

def calculate_wu_palmer(dataset):
    for row in dataset:
        first_elem_synset=wordnet.synsets(row[0])
        second_elem_synset = wordnet.synsets(row[1])
        max=-1
        for first_synset in first_elem_synset:
            for second_synset in second_elem_synset:
                first_elem_height=first_synset.max_depth()+1
                second_elem_height=second_synset.max_depth()+1
                break_loop=True
                while(break_loop):
                    if(first_synset == second_synset):
                     break_loop=False
                    elif(first_synset.max_depth() > second_synset.max_depth()):
                        hyper=first_synset.hypernyms()
                        if(len(hyper)>0):
                            first_synset = hyper[0]
                        else:
                            break_loop=False
                            first_elem_height=-1
                    else:
                        hyper = second_synset.hypernyms()
                        if (len(hyper) > 0):
                            second_synset = hyper[0]
                        else:
                            break_loop = False
                            second_elem_height = -1
                lcs_height=first_synset.max_depth()+1
                if(first_elem_height>=0 and second_elem_height>=0):
                    index=((2*lcs_height)/(first_elem_height+second_elem_height))*10
                else:
                    index=-1
                if(index>max):
                    max=index
        row[3]=max
    return dataset

def calculate_shortest_path(dataset):
    for row in dataset:
        first_elem_synset=wordnet.synsets(row[0])
        second_elem_synset = wordnet.synsets(row[1])
        max_depth = WN_3_1_MAX_DEPTH
        max=-1
        for first_synset in first_elem_synset:
            for second_synset in second_elem_synset:
                steps=0
                break_loop=True
                while(break_loop):
                    if(first_synset == second_synset):
                     break_loop=False
                    elif(first_synset.max_depth() > second_synset.max_depth()):
                        hyper=first_synset.hypernyms()
                        if(len(hyper)>0):
                            first_synset = hyper[0]
                        else:
                            break_loop=False
                            steps=-2
                    else:
                        hyper = second_synset.hypernyms()
                        if (len(hyper) > 0):
                            second_synset = hyper[0]
                        else:
                            break_loop = False
                            steps = -2
                    steps+=1
                if(steps>=0):
                    index=index=normalize(((2*max_depth)-steps),0,(2*max_depth))*10
                else:
                    index=-1
                if(index>max):
                    max=index
        row[4]=max
    return dataset

def calculate_leakcock_chodorow(dataset):
    for row in dataset:
        first_elem_synset=wordnet.synsets(row[0])
        second_elem_synset = wordnet.synsets(row[1])
        max_depth = WN_3_1_MAX_DEPTH
        max = -1
        for first_synset in first_elem_synset:
            for second_synset in second_elem_synset:
                steps=0
                break_loop=True
                while(break_loop):
                    if(first_synset == second_synset):
                     break_loop=False
                    elif(first_synset.max_depth() > second_synset.max_depth()):
                        hyper=first_synset.hypernyms()
                        if(len(hyper)>0):
                            first_synset = hyper[0]
                        else:
                            break_loop=False
                            steps=-2
                    else:
                        hyper = second_synset.hypernyms()
                        if (len(hyper) > 0):
                            second_synset = hyper[0]
                        else:
                            break_loop = False
                            steps = -2
                    steps+=1
                if(steps>=0):
                    index=normalize((-1*math.log((steps+1)/((2*max_depth)+1))),0,math.log(2*max_depth+1))*10
                else:
                    index=-1
                if(index>max):
                    max=index
        row[5]=max
    return dataset




if __name__ == "__main__":
    dataset=read_csv("WordSim353/WordSim353/WordSim353.csv")
    dataset=calculate_wu_palmer(dataset)
    dataset=calculate_shortest_path(dataset)
    dataset=calculate_leakcock_chodorow(dataset)

    human_coefficents=[row[2] for row in dataset]
    wu_coefficents=[row[3] for row in dataset]
    shortest_coefficents=[row[4] for row in dataset]
    leak_coefficents=[row[5] for row in dataset]

    correlation_coefficient,p_value = pearsonr(human_coefficents, wu_coefficents)
    print("Perason for Wu Palmer: ",str(correlation_coefficient))
    correlation_coefficient,p_value = spearmanr(human_coefficents, wu_coefficents)
    print("Spearman rank for Wu Palmer: ",str(correlation_coefficient),"\n")

    correlation_coefficient,p_value = pearsonr(human_coefficents, shortest_coefficents)
    print("Perason for Shortest Path: ", str(correlation_coefficient))
    correlation_coefficient,p_value = spearmanr(human_coefficents, shortest_coefficents)
    print("Spearman rank for Shortest Path: ",str(correlation_coefficient),"\n")


    correlation_coefficient,p_value = pearsonr(human_coefficents, leak_coefficents)
    print("Perason for Leakcock & Chodorow: ", str(correlation_coefficient))
    correlation_coefficient,p_value = spearmanr(human_coefficents, leak_coefficents)
    print("Spearman rank for Leakcock & Chodorow: ",str(correlation_coefficient),"\n")

    print(dataset)
#+ vicino a 1 è più sono correlate, + vicino a meno -1 è più sono inversamente correlate, vicino a 0 no correlazione