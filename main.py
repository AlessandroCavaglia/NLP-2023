from ObiChatKenobi.ApiApplication.dialogueManager import DialogueManager
from ObiChatKenobi.ApiApplication.language_understanding import LanguageUnderstanding

if __name__ == "__main__":
    understanding=LanguageUnderstanding()
    dialogueManager=DialogueManager()
    while(len(dialogueManager.questionsToAsk)>0):
        systemDialogueAct=dialogueManager.getQuestion()
        print(systemDialogueAct.phrase)
        speechRecognitionHypotesis = input()
        userDialogueAct=understanding.understand_answer(speechRecognitionHypotesis,systemDialogueAct.answerVerbs)
        dialogueManager.answerQuestion(userDialogueAct)
