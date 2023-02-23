import numpy as np
import random
import json
import nltk
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD
from nltk.stem import WordNetLemmatizer



lemmatizer = WordNetLemmatizer()
intents_file = "intents.json"

with open(intents_file, 'r', encoding='utf-8') as file:
    data = json.load(file)

words = []
classes = []
documents = []
ignore = ["?", "!", ".", ","]

# Traitement de la liste d'intents
for intent in data["intents"]:
    for pattern in intent["patterns"]:
        # Tokenisation
        words_list = nltk.word_tokenize(pattern)
        words.extend(words_list)
        # Création de la liste de documents
        documents.append((words_list, intent["tag"]))
        # Ajout de la classe
        if intent["tag"] not in classes:
            classes.append(intent["tag"])

# Lemmatisation des mots
words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore]
words = sorted(list(set(words)))
classes = sorted(list(set(classes)))

# Création des données d'entrée et de sortie
training = []
output = []
output_empty = [0] * len(classes)
for doc in documents:
    bag = []
    words_list = doc[0]
    words_list = [lemmatizer.lemmatize(w.lower()) for w in words_list]
    for w in words:
        bag.append(1) if w in words_list else bag.append(0)
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1
    training.append([bag, output_row])

# Conversion des données en numpy array pour l'entrainement
random.shuffle(training)
training = np.array(training, dtype=object)
train_x = list(training[:, 0])
train_y = list(training[:, 1])

# Création du modèle
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

# Compilation du modèle
sgd = SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

# Entrainement du modèle
model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)

# Sauvegarde du modèle
model.save('chatbot_model.h5')