import random


class Question:
    def __init__(self, phrases, answerVerbs, correctAnswers, describedAnswers):
        self.phrase = ""
        self.phrases = phrases
        self.answerVerbs = answerVerbs
        self.correctAnswers = correctAnswers
        self.describedAnswers = describedAnswers


class Phrase:
    def __init__(self, phrase, sentiment):
        self.phrase = phrase
        self.sentiment = sentiment


class Frame:
    def __init__(self, remainingQuestions, correctAnswers, incorrectAnswers, lastAction):
        self.remainingQuestions = remainingQuestions
        self.correctAnswers = correctAnswers
        self.incorrectAnswers = incorrectAnswers
        self.lastAction = lastAction

    def match(self, otherFrame):
        ret = True
        if self.remainingQuestions != -1 and self.remainingQuestions > otherFrame.remainingQuestions:
            ret = False
        if self.correctAnswers != -1 and self.correctAnswers > otherFrame.correctAnswers:
            ret = False
        if self.incorrectAnswers != -1 and self.incorrectAnswers > otherFrame.incorrectAnswers:
            ret = False
        if self.lastAction != "*" and self.lastAction != otherFrame.lastAction:
            ret = False
        return ret


FAILED_TEST = Frame(-1, -1, 4, "*")
PASSED_TEST = Frame(-1, 4, -1, "*")
START_TEST = Frame(-1, -1, -1, "START")
WRONG_ANSWER_FRAME = Frame(-1, -1, -1, "FALSE")
CORRECT_ANSWER_FRAME = Frame(-1, -1, -1, "TRUE")
UNKNOWN_ANSWER_FRAME = Frame(-1, -1, -1, "UNK")


class DialogueManager:
    def __init__(self):
        self.questionsToAsk = []
        self.currentSentiment = 1
        self.welcomAntePhrases = []
        self.correctAntePhrases = []
        self.incorrectAntePhrases = []
        self.failedTestPhrases = []
        self.passedTestPhrases = []
        self.unknownAntePhrases = []
        self.askedQuestion = None
        self.chosenWelcomAntePhrase = None
        self.chosenCorrectAntePhrases = None
        self.chosenIncorrectAntePhrases = None
        self.chosenUnknownAntePhrases = None
        self.correctAnswers = 0
        self.wrongAnswers = 0
        self.dialogueAction = [("START", "START")]
        self.questionsToAsk.append(Question(
            ["What is the core component of a light-saber?", "What is the most important part of a light-saber?"],
            ["be", "make"], [['kyber crystal'], ['kyber-crystal'], ['a kyber-crystal'], ['crystal']],
            ["Kyber crystal was the right answer, let's move on, ",
             "the correct answer is kyber crystal, it's an important subject youngling, let's move on, "]))
        self.questionsToAsk.append(Question(["Can a jedi use the force for personal gain?",
                                             "If you will become a jedi, can you use the force for personal gain?"],
                                            ["can", "be"], [['no'], ['not']],
                                            ["a jedi can't and never will use the force for personal gain! Now "
                                                "let's go to the next question: ",
                                                "a jedi absolutely can't use the force for personal gain! let's keep "
                                                "going: "]))
        self.questionsToAsk.append(
            Question(["can a jedi get involved in a relationship?", "can a jedi get into a romantic relationship?"],
                     ["be", "can"], [['no'], ['not']],
                     ["a jedi can't let his emotions win over his connection with the force, let's go on and try "
                         "with another question: ",
                         "you must calm your horses, a jedi can't get involved, the force is our only love, "
                         "let's move on"]))
        self.questionsToAsk.append(
            Question(["where is the jedi temple located?"], ["be", "locate", "reside"], [['coruscant']],
                     ["our temple is located on Coruscant let's keep going to the next question: ",
                      "our temple and our council resides in Coruscant, let's move on"]))
        self.questionsToAsk.append(Question(["As jedis we work to bring the force to which state?"], ["be", "bring"],
                                            [['balance'], ['balanced'], ['state of balance']],
                                            [
                                                "as jedis we work to bring balance to the force, let's keep going to "
                                                "the next question: ",
                                                "our goal is to keep balance to the force, let's move on"]))
        self.questionsToAsk.append(Question(["what are the three main pillars of Jedi training?"], ["be"],
                                            [['knowledge', '&', 'defense', '&', 'armony'],
                                             ['defense', '&', 'knowledge', '&', 'armony'],
                                             ['armony', '&', 'defense', '&', 'knowledge'],
                                             ['defense', '&', 'armony', '&', 'knowledge'],
                                             ['defense', '&', 'knowledge', '&', 'armony']],
                                            [
                                                "the three main pillars are knowledge,defense,armony, let's keep "
                                                "going to the next question: "]))

        self.questionsToAsk.append(Question(["What type of colour of the lightsaber represents the Jedi Consular?","Which colour of lightsaber should a member of the jedi council hold?"], ["be","represent","hold"],
                                            [["green"]],
                                            [
                                                "The lightsaber should be green young student, be obedient when you see one of that colour! let's move on",
                                                "The answer was green. let's keep going! "]))

        self.questionsToAsk.append(Question(["Which ancient Jedi artifact holds the knowledge of past jedi masters?",
                                             "What's the name of the artifact that holds the knowledge of the most important jedi masters of the past?"],
                                            ["be"],
                                            [["jedi holocron"],["holocron"]],
                                            [
                                                "You must know the history to be prepared for the future, the answer was the famous Jedi Holocron, let's move on ",
                                                "This is very important young student,the answer was the Jedi Holocron, let's move to the next question and see if you have studied "]))
        self.questionsToAsk.append(Question(["Which legendary Jedi and mandalorian wielded the single-bladed lightsaber known as the Darksaber?",
                                             "Who was the famous jedi mandalorian that was known for wielding the Darksaber?"],
                                            ["be"],
                                            [["pre vizsla"]],
                                            [
                                                "His name was a legend, he was Pre Vizsla, i can't belive you don't know him, let's move on ",
                                                "He was Pre Vizsla, the only jedi mandalorian, let's keep going "]))
        self.questionsToAsk.append(Question(["Which Jedi master was the first to discover the secret to maintaining  consciousness after death and manifest to others?",
                                             "Which Jedi master was the first to manifest as a force ghost?"],
                                            ["be"],
                                            [["qui-gon jinn"],["qui-gon"],["qui gon"],["qui gon jinn"]],
                                            [
                                                "His name was Qui-Gon Jinn, he was my master, let's move to the next question "
                                                "His name was Qui-Gon Jinn, i was his padawan, let's move on "]))

        self.welcomAntePhrases.append(Phrase(
            "Welcome young student! Thrilled to become a jedi? This if your first question to check if you have what is needed: ",
            1))
        self.welcomAntePhrases.append(Phrase(
            "Hello there! Are you ready to become a jedi? Let's see if you have studied enough: ", 1))

        self.failedTestPhrases.append(Phrase(
            "Young student, you clearly aren't prepared, don't let the dark side consume you and try again next time.",
            0))
        self.failedTestPhrases.append(Phrase(
            "Sorry young student, but you haven't studied enough for this test! Try again in a while and you will "
            "succseed.",
            1))
        self.failedTestPhrases.append(Phrase(
            "I'm really sorry student but you haven't passed the exam, if you need help to study you can ask me any "
            "time.",
            2))

        self.passedTestPhrases.append(Phrase(
            "Well you clearly studied, you can become a padawan but be careful about the dark side, "
            "i feel disturbance in you soul.",
            0))
        self.passedTestPhrases.append(Phrase(
            "Congratulations you have studied, you have passed the test and can officially  become a padawan! Good luck "
            "on becoming a Jedi.",
            1))
        self.passedTestPhrases.append(Phrase(
            "I'm amazed from your performance, you clearly have what it needs to become a good padawan and hopefully "
            "a good Jedi.",
            2))

        self.correctAntePhrases.append(
            Phrase("Correct but this question was simple. Let's keep going, next question: ", 0))
        self.correctAntePhrases.append(Phrase("It's correct. Let's keep going, next question: ", 1))
        self.correctAntePhrases.append(Phrase("Good answer! Let's keep going, next question: ", 2))

        self.incorrectAntePhrases.append(Phrase("That's not right! you must study more!! ", 0))
        self.incorrectAntePhrases.append(Phrase("That's not right! ", 1))
        self.incorrectAntePhrases.append(Phrase("That's not right! but don't lose your belief, ", 2))

        self.unknownAntePhrases.append(
            Phrase("Sorry youngling but i can't understand you, could you answer me again: ", 0))
        self.unknownAntePhrases.append(
            Phrase("Sorry youngling but i can't understand you, could you answer me again: ", 1))
        self.unknownAntePhrases.append(
            Phrase("Sorry youngling but i can't understand you, could you answer me again: ", 2))

    def getQuestion(self):
        converstaionStatus = Frame(len(self.questionsToAsk), self.correctAnswers, self.wrongAnswers,
                                   self.dialogueAction[len(self.dialogueAction) - 1][1])
        if FAILED_TEST.match(converstaionStatus):
            self.askedQuestion = Question([], [], [], [])
            self.askedQuestion.phrase = random.choice(
                [p.phrase for p in self.failedTestPhrases if p.sentiment == self.currentSentiment])
        elif PASSED_TEST.match(converstaionStatus):
            self.askedQuestion = Question([], [], [], [])
            self.askedQuestion.phrase = random.choice(
                [p.phrase for p in self.passedTestPhrases if p.sentiment == self.currentSentiment])
        elif START_TEST.match(converstaionStatus):  # It means we are starting the conversation
            self.askedQuestion = random.choice(self.questionsToAsk)
            self.questionsToAsk.remove(self.askedQuestion)
            self.chosenWelcomAntePhrase = random.choice([p.phrase for p in self.welcomAntePhrases if
                                                         p.sentiment == self.currentSentiment])  # filtered by sentiment
            self.askedQuestion.phrase = self.chosenWelcomAntePhrase + random.choice(
                self.askedQuestion.phrases)
        elif CORRECT_ANSWER_FRAME.match(converstaionStatus):
            self.askedQuestion = random.choice(self.questionsToAsk)
            self.questionsToAsk.remove(self.askedQuestion)
            self.chosenCorrectAntePhrases = random.choice(
                [p.phrase for p in self.correctAntePhrases if
                 p.sentiment == self.currentSentiment])  # filtered by sentiment
            self.askedQuestion.phrase = self.chosenCorrectAntePhrases + random.choice(
                self.askedQuestion.phrases)
        elif WRONG_ANSWER_FRAME.match(converstaionStatus):
            wrongQuest = self.askedQuestion
            self.askedQuestion = random.choice(self.questionsToAsk)
            self.questionsToAsk.remove(self.askedQuestion)
            self.chosenIncorrectAntePhrases = random.choice(
                [p.phrase for p in self.incorrectAntePhrases if
                 p.sentiment == self.currentSentiment])  # filtered by sentiment
            self.askedQuestion.phrase = self.chosenIncorrectAntePhrases + random.choice(
                wrongQuest.describedAnswers) + random.choice(
                self.askedQuestion.phrases)

        elif UNKNOWN_ANSWER_FRAME.match(converstaionStatus):
            self.chosenUnknownAntePhrases = random.choice(
                [p.phrase for p in self.unknownAntePhrases if
                 p.sentiment == self.currentSentiment])  # filtered by sentiment
            self.askedQuestion.phrase = self.chosenUnknownAntePhrases + random.choice(
                self.askedQuestion.phrases)

        return self.askedQuestion

    def answerQuestion(self, answers):
        if (answers == None):
            return
        self.currentSentiment = answers.sentiment
        trueAnswer = "FALSE"
        if (
                None in answers.complements or None in answers.verbs or None in answers.modifiers):  # If our parsing trew an exception it means we didn't understand the answer
            trueAnswer = "UNK"
        else:  # We understood the answer so we check if it is correct
            for sol in self.askedQuestion.correctAnswers:
                if (sol in answers.complements):
                    trueAnswer = "TRUE"
                for sol_elem in sol:
                    for complement in answers.complements:
                        for compl_elem in complement:
                            if(sol_elem in compl_elem):
                                trueAnswer= "TRUE"
            '''for phrase in answers.complements:
                for elem in phrase:
                    if (elem.lower() in self.askedQuestion.correctAnswers):
                        trueAnswer = "TRUE"'''
        if trueAnswer == "TRUE":
            self.correctAnswers += 1
        if trueAnswer == "FALSE":
            self.wrongAnswers += 1
        self.dialogueAction.append((self.askedQuestion, trueAnswer))
