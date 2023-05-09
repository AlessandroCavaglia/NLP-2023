from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import pickle
from .dialogueManager import DialogueManager
from .models import languageUnderstanding
import codecs

# Create your views here.
class BotApiView(APIView):
    def get(self, request):
        if 'dialogueManager' in request.session:
            print("Bentornato")
            dialogueManager=pickle.loads(codecs.decode(request.session['dialogueManager'].encode(), "base64"))
        else:
            print("Benvenuto")
            pickledDialogueManager = codecs.encode(pickle.dumps(DialogueManager()),"base64").decode()  # Pickling the object
            request.session['dialogueManager']=pickledDialogueManager


        return Response({"Message": "Ciao a tutti"})

