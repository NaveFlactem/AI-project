import os
import random
import json
import pickle
import numpy as np
import nltk
import tkinter as tk
import spellchecker as sp
from nltk.stem import WordNetLemmatizer
from keras.models import load_model

class ChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chatbot GUI")

        self.chat_history = tk.Listbox(self.root, width=50, height=20)
        self.chat_history.pack(pady=10)

        self.scrollbar = tk.Scrollbar(self.root, command=self.chat_history.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.chat_history.config(yscrollcommand=self.scrollbar.set)

        self.user_input = tk.Entry(self.root, width=50)
        self.user_input.pack(pady=10)
        self.user_input.bind("<Return>", lambda event: self.send_message())

        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_button.pack()

        self.lemmatizer = WordNetLemmatizer()
        script_directory = os.path.dirname(os.path.abspath(__file__))
        self.intents = json.loads(open(os.path.join(script_directory, 'intents.json')).read())
        self.words = pickle.load(open('words.pkl', 'rb'))
        self.classes = pickle.load(open('classes.pkl', 'rb'))
        self.model = load_model('chatbot_model.h5')

    def spell_check(self, sentence):
        spell = sp.SpellChecker()
        sentence_words = nltk.word_tokenize(sentence)
        misspelled = spell.unknown(sentence_words)
        for word in misspelled:
            sentence = sentence.replace(word, spell.correction(word))
        return sentence

    def clean_up_sentence(self, sentence):
        sentence_words = nltk.word_tokenize(sentence)
        sentence_words = [self.lemmatizer.lemmatize(word) for word in sentence_words]
        return sentence_words

    def bag_of_words(self, sentence):
        sentence_words = self.clean_up_sentence(sentence)
        bag = [0] * len(self.words)
        for w in sentence_words:
            for i, word in enumerate(self.words):
                if word == w:
                    bag[i] = 1
        return np.array(bag)

    def predict_class(self, sentence):
        bow = self.bag_of_words(sentence)
        res = self.model.predict(np.array([bow]))[0]
        ERROR_THRESHOLD = 0.25
        results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in results:
            return_list.append({'intent': self.classes[r[0]], 'probability': str(r[1])})
        return return_list

    def get_response(self, intents_list, intents_json):
        tag = intents_list[0]['intent']
        list_of_intents = intents_json['intents']
        for i in list_of_intents:
            if i['tag'] == tag:
                result = random.choice(i['responses'])
                break
        return result

    def send_message(self):
        message = self.user_input.get()
        self.user_input.delete(0, tk.END)
        self.chat_history.insert(tk.END, "You: " + message)
        self.chat_history.insert(tk.END, "Bot: " + self.get_response(self.predict_class(message), self.intents))
        self.chat_history.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatbotGUI(root)
    root.mainloop()
