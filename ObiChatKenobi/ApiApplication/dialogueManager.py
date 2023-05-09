import random

class Question:
    def __init__(self,phrases,answerVerbs,correctAnswers,describedAnswers):
        self.phrase=""
        self.phrases=phrases
        self.answerVerbs=answerVerbs
        self.correctAnswers=correctAnswers
        self.describedAnswers=describedAnswers

class DialogueManager:
    def __init__(self):
        self.questionsToAsk=[]
        self.welcomAntePhrases=[]
        self.correctAntePhrases=[]
        self.incorrectAntePhrases=[]
        self.unknownAntePhrases=[]
        self.askedQuestion=None
        self.dialogueAction=[("START","START")]
        self.questionsToAsk.append(Question(["how old is a 7 years old?"], ["be"], ["7", "7 years", "7 years old"],["7 years old was the right answer, let's move on, "]))
        self.questionsToAsk.append(Question(["in which country does Rome reside"], ["be", "reside"], ["italy"],["it resides in Italy, but now let's go to the next question: ","last time i check it was in Italy! But i may be wrong, let's keep going: "]))
        self.questionsToAsk.append(Question(["can a priest get married?"], ["be", "can"], ["no", "not"],["he absolutely can't, let's go on and try with another question: "]))


        self.welcomAntePhrases.append("Welcome young student! Thrilled to become a jedi? This if your first question to check if you are good: ")
        self.welcomAntePhrases.append("Hello there! Are you ready to become a jedi? Let's see if you have studied enough: ")

        self.correctAntePhrases.append("Good answer! let's keep going, next question: ")

        self.incorrectAntePhrases.append("That's not right! ")

        self.unknownAntePhrases.append("Sorry youngling but i can't understand you, could you answer me again: ")


    def getQuestion(self):
        if(self.dialogueAction[len(self.dialogueAction)-1][1]=="START"):    #It means we are starting the conversation
            self.askedQuestion = random.choice(self.questionsToAsk)
            self.questionsToAsk.remove(self.askedQuestion)
            self.askedQuestion.phrase = random.choice(self.welcomAntePhrases) + random.choice(self.askedQuestion.phrases)
        elif(self.dialogueAction[len(self.dialogueAction)-1][1]=="TRUE"):
            self.askedQuestion = random.choice(self.questionsToAsk)
            self.questionsToAsk.remove(self.askedQuestion)
            self.askedQuestion.phrase = random.choice(self.correctAntePhrases) + random.choice(
                self.askedQuestion.phrases)
        elif (self.dialogueAction[len(self.dialogueAction) - 1][1] == "FALSE"):
            wrongQuest= self.askedQuestion
            self.askedQuestion = random.choice(self.questionsToAsk)
            self.questionsToAsk.remove(self.askedQuestion)
            self.askedQuestion.phrase = random.choice(self.incorrectAntePhrases)+random.choice(wrongQuest.describedAnswers) + random.choice(
                self.askedQuestion.phrases)

        elif (self.dialogueAction[len(self.dialogueAction) - 1][1] == "UNK"):
            self.askedQuestion.phrase = random.choice(self.unknownAntePhrases)+ random.choice(
                self.askedQuestion.phrases)



        return self.askedQuestion

    def answerQuestion(self,answers):
        trueAnswer="FALSE"
        if(None in answers.complements or None in answers.verbs or None in answers.modifiers): #If our parsing trew an exception it means we didn't understand the answer
            trueAnswer="UNK"
        else: #We understood the answer so we check if it is correct
            for phrase in answers.complements:
                for elem in phrase:
                    if(elem.lower() in self.askedQuestion.correctAnswers):
                        trueAnswer="TRUE"
        self.dialogueAction.append((self.askedQuestion,trueAnswer))