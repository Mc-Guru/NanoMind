import random
import json
import nltk
import numpy as np
from tensorflow.keras.models import load_model
from nltk.stem import WordNetLemmatizer
import os.path
import requests
import subprocess
from datetime import datetime
from pywinauto.application import Application

# -*- coding: utf-8 -*-

now = datetime.now()
current_time = now.strftime("%Hh%M")


lemmatizer = WordNetLemmatizer()
intents_file = "intents.json"
# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('omw-1.4')

with open(intents_file, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Chargement des mots et classes depuis le fichier intents.json
words = []
classes = []
documents = []
ignore = ["?", "!", ".", ","]
for intent in data["intents"]:
    for pattern in intent["patterns"]:
        words_list = nltk.word_tokenize(pattern)
        words.extend(words_list)
        documents.append((words_list, intent["tag"]))
        if intent["tag"] not in classes:
            classes.append(intent["tag"])

words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore]
words = sorted(list(set(words)))
classes = sorted(list(set(classes)))


# Chargement du modèle
model = load_model("chatbot_model.h5")


# Fonction pour prétraiter le message de l'utilisateur
def clean_up_sentence(sentence):
    sentence = sentence.replace("koa", "quoi")
    sentence = sentence.replace("à", "a")
    sentence = sentence.replace("kwa", "quoi")
    sentence = sentence.replace("chui", "je suis")
    sentence = sentence.replace("jsuis", "je suis")
    sentence = sentence.replace("j'suis", "je suis")
    sentence = sentence.replace("c", "c'est")
    sentence = sentence.replace("chuis", "je suis")
    sentence = sentence.replace("jsp", "je sais pas")
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# Fonction pour créer un sac de mots à partir du message de l'utilisateur
def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

# Fonction pour prédire la classe de l'intent
def predict_class(message):
    message_words = nltk.word_tokenize(message)
    message_words = [lemmatizer.lemmatize(word.lower()) for word in message_words]
    bag_of_words = [0] * len(words)
    for w in message_words:
        for i, word in enumerate(words):
            if word == w:
                bag_of_words[i] = 1
    result = model.predict(np.array([bag_of_words]))[0]
    predicted_class = classes[np.argmax(result)]
    probability = result[np.argmax(result)]
    return predicted_class, probability

import subprocess

#...

def get_response(predicted_class, probability, intents_data):
    for intent in intents_data["intents"]:
        if intent['tag'] == predicted_class:
            if probability < 0.84:
                return "Je suis désolé, je ne comprends pas de quoi vous parlez"
            else:
                if predicted_class == "time":
                    response = "Il est " + current_time
            if predicted_class == "antivirus":
                # tentative d'ouverture de l'application antivirus
                app = Application().start("NanoProtect.exe")
                response = "Neurolink travaille activement sur un antivirus, je vous le montre"
            else:
                response = random.choice(intent['responses'])
            return response

# Boucle principale pour l'interaction avec l'utilisateur
print("Discussion entre vous et le chatbot")
while True:
    message = input("Vous: ")
    if message in ["quitter", "quit", "q"]:
        break
    if len(message) < 2:
        print("Bot: Votre message n'est pas assez long.")
        continue
    predicted_class, probability = predict_class(message)
    response = get_response(predicted_class, probability, data)
    print("Bot : " + response + "  (" + str(probability) + ")")