import json

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import pickle
from .dialogueManager import DialogueManager
from .language_understanding import LanguageUnderstanding
from .models import languageUnderstanding
import codecs

# Create your views here.
understanding=LanguageUnderstanding()


def home(request):
    return render(request, 'index.html')


def css(request):
    return render(request, 'main.css')


def js(request):
    return render(request, 'main.js',content_type='text/plain')
class BotApiView(APIView):

    def post(self, request, *args, **kwargs):
        data=json.loads(request.body)
        print(data)
        dialogueManager=None
        #LOAD THE DIALOGUEMANAGER
        if 'dialogueManager' in request.session:
            dialogueManager=pickle.loads(codecs.decode(request.session['dialogueManager'].encode(), "base64"))
        else:
            dialogueManager=DialogueManager()

        if(dialogueManager.askedQuestion!=None):
            userDialogueAct = understanding.understand_answer(data['speechRecognitionHypotesis'], dialogueManager.askedQuestion.answerVerbs)
            dialogueManager.answerQuestion(userDialogueAct)
        systemDialogueAct = dialogueManager.getQuestion()

        # SAVE THE DIALOGUEMANAGER
        pickledDialogueManager = codecs.encode(pickle.dumps(dialogueManager),"base64").decode()  # Pickling the object
        request.session['dialogueManager'] = pickledDialogueManager
        res=Response({"Message": systemDialogueAct.phrase})
        return res

