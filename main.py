import tkinter as tk
from tkinter import Scrollbar, Listbox, Entry, Button

class ChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chatbot GUI")
        
        #initialize the chatbox
        self.chat_log = Listbox(root, width=100, height=20)
        self.chat_log.pack(padx=10, pady=10)
        #color
        self.chat_log.config(bg="light gray", fg="gray", justify=tk.LEFT, activestyle=tk.NONE, highlightthickness=0, highlightcolor="light gray", highlightbackground="light gray", bd=0, font=("Verdana", 12))

        
        #add the scroll feature
        self.scrollbar = Scrollbar(root, command=self.chat_log.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.chat_log.config(yscrollcommand=self.scrollbar.set)
        
        #Entry box
        self.entry = Entry(root, width=40)
        self.entry.pack(padx=10, pady=10)
        
        #Send Button
        self.send_button = Button(root, text="Send", command=self.send_message)
        self.send_button.pack()
        self.entry.bind("<Return>", lambda x: self.send_message())
        
        ####Place Holder responses
        self.chatbot_responses = {
            "hello": "Hello there!",
            "how are you": "Good enough",
        }
        ######
        
    def send_message(self):
        user_message = self.entry.get()
        self.chat_log.insert(tk.END, "You: " + user_message)
        self.entry.delete(0, tk.END)
        
        bot_response = self.get_bot_response(user_message)
        self.chat_log.insert(tk.END, "Bot: " + bot_response)
        



    def get_bot_response(self, user_message):
        user_message = user_message.lower()
        response = self.chatbot_responses.get(user_message, "I'm not sure how to respond to that.")
        return response



if __name__ == "__main__":
    root = tk.Tk()
    app = ChatbotGUI(root)
    root.mainloop()
