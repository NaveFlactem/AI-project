import json
import tkinter as tk
from tkinter import simpledialog
from datetime import datetime  # Added for timestamp
from difflib import get_close_matches

class ChatBot:
    def __init__(self):
        self.knowledge_base = self.load_knowledge_base('knowledge_base.json')
        self.conversations = {}  # Dictionary to store conversation histories
        self.current_conversation_id = self.generate_conversation_id()  # Current conversation ID
        self.create_conversation(self.current_conversation_id)  # Load or create a default conversation

    def generate_conversation_id(self) -> str:
        return datetime.now().strftime('%Y%m%d%H%M%S')

    def load_knowledge_base(self, file_path: str) -> dict:
        with open(file_path, 'r') as f:
            knowledge_base = json.load(f)
        return knowledge_base

    def save_knowledge_base(self, file_path: str) -> None:
        with open(file_path, 'w') as f:
            json.dump(self.knowledge_base, f, indent=2)

    def create_conversation(self, conversation_id):
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = []  # Create a new conversation history
        self.current_conversation_id = conversation_id
    
    def load_history(self, file_path: str) -> dict:
        try:
            with open(file_path, 'r') as f:
                conversations = json.load(f)
        except FileNotFoundError:
            conversations = {}  # Create an empty dictionary if the file doesn't exist
        return conversations

    def save_history(self, file_path: str) -> None:
        with open(file_path, 'w') as f:
            json.dump(self.conversations, f, indent=2)

    def find_best_match(self, user_question: str, questions: list[str]) -> str | None:
        matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
        return matches[0] if matches else None

    def get_answer_for_question(self, question: str) -> str | None:
        for q in self.knowledge_base["questions"]:
            if q['question'] == question:
                return q['answer']

    def collect_user_input(self, user_input):
        user_response = simpledialog.askstring("User Input", user_input)
        return user_response
    
    def insert_message(self, chat_text, message):
        if message.startswith("Bot:"):
            tag = "bot"
        elif message.startswith("User:"):
            tag = "user"
        else:
            tag = "info"
        
        chat_text.insert(tk.END, message)
        chat_text.itemconfigure(tk.END, {'bg': "light gray" if tag == "user" else "white", 'fg': "black" if tag == "user" else "black"})
        chat_text.itemconfigure(tk.END, {})


    def update_chat(self, user_input, chat_text, user_entry):
        user_message = f"User: {user_input}\n"
        self.insert_message(chat_text, user_message)
        conversation_history = ''.join([f"{message['message']}\n" for message in self.conversations[self.current_conversation_id]])
        conversation_history += user_message

        best_match: str | None = self.find_best_match(conversation_history, [q['question'] for q in self.knowledge_base["questions"]])

        if best_match:
            answer: str = self.get_answer_for_question(best_match)
            response = f"Bot: {answer}\n"
        else:
            response = "Bot: Sorry, I don't know what to say. Can you teach me?\n"
            self.insert_message(chat_text, response)

            response = "\nType the answer to your prompt or type 'skip' to skip: "
            self.insert_message(chat_text, response)

            new_answer: str = self.collect_user_input(response)

            if new_answer and new_answer.lower() != 'skip':
                self.knowledge_base["questions"].append({"question": conversation_history, "answer": new_answer})
                self.save_knowledge_base('knowledge_base.json')
                response = "\nBot: Thanks, I'll remember that.\n"
            else:
                response = "\nBot: Okay, I'll skip.\n"

        self.insert_message(chat_text, response)
        user_entry.delete(0, tk.END)
        chat_text.yview(tk.END)

        # Timestamp for the current message
        current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        message = {"message": user_message, "timestamp": current_timestamp}
        
        # Update conversation history
        self.conversations[self.current_conversation_id].append(message)
        self.save_history('history.json')

    def send_message(self, event, user_entry, message_list):
        user_input = user_entry.get()
        if user_input.lower() == '-exit-':
            exit()
        self.update_chat(user_input, message_list, user_entry)

    def overwrite_button(self):
        conversation_history = ''.join([f"{message['message']}\n" for message in self.conversations[self.current_conversation_id]])
        response = "\nType the answer to your prompt or type 'skip' to skip: "
        new_answer: str = self.collect_user_input(response)

        if new_answer and new_answer.lower() != 'skip':
            self.knowledge_base["questions"].append({"question": conversation_history, "answer": new_answer})
            self.save_knowledge_base('knowledge_base.json')
            response = "\nBot: Thanks, I'll remember that.\n"
        else:
            response = "\nBot: Okay, I'll skip.\n"


    def adjust_message_width(message_list):
        desired_width = int(message_list.winfo_width() * 0.8)
        message_list.configure(width=desired_width)
    
    def run(self):
        root = tk.Tk()
        root.title("Chat Bot")

        initial_width = 800
        initial_height = 600

        root.geometry(f"{initial_width}x{initial_height}")
        root.minsize(initial_width, initial_height)

        root.configure(bg='black')
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=4)
        root.rowconfigure(0, weight=1)

        ########### History Frame ############
        history_frame = tk.Frame(root)
        history_frame.grid(row=0, column=0, sticky='nsew')
        history_frame.columnconfigure(0, weight=1)
        history_frame.rowconfigure(0, weight=1)

        history_list = tk.Listbox(history_frame, bg='beige', fg='white', font=('Times New Roman', 15), justify='left', borderwidth=5)
        history_list.grid(row=0, column=0, sticky='nsew')

        # Create a vertical scrollbar for the history Listbox
        history_scrollbar = tk.Scrollbar(history_frame, command=history_list.yview)
        history_scrollbar.grid(row=0, column=1, sticky='ns')
        history_list.config(yscrollcommand=history_scrollbar.set)
        #######################################

        ########### Message Frame ############
        message_frame = tk.Frame(root)
        message_frame.grid(row=0, column=1, sticky='nsew')
        message_frame.columnconfigure(0, weight=1)
        message_frame.rowconfigure(0, weight=1)

        # Create a vertical scrollbar for the Listbox
        message_scrollbar = tk.Scrollbar(message_frame)
        message_scrollbar.grid(row=0, column=1, sticky='ns')

        message_list = tk.Listbox(message_frame, bg='black', fg='white', font=('Times New Roman', 15), justify='left', borderwidth=5, yscrollcommand=message_scrollbar.set)
        message_list.grid(row=0, column=0, sticky='nsew')
        #######################################

        #####>
        history_scrollbar.grid_forget()
        message_scrollbar.grid_forget()
        #####>

        ########### Mouse Binds ############
        history_list.bind('<Enter>', lambda event: self.show_history_scrollbar(history_scrollbar))
        history_list.bind('<Leave>', lambda event: self.hide_scrollbar(history_scrollbar))
        message_list.bind('<Enter>', lambda event: self.show_message_scrollbar(message_scrollbar))
        message_list.bind('<Leave>', lambda event: self.hide_scrollbar(message_scrollbar))


        ########### User Entry ############
        user_entry = tk.Entry(root, bg='dark gray', fg='white', font=('Times New Roman', 15), justify='left', borderwidth=5, width=60)
        user_entry.place(relx=0.6, rely=0.9, anchor='center')
        user_entry.bind("<Return>", lambda event: self.send_message(event, user_entry, message_list))

        send_button = tk.Button(root, text="Send", bg='white', fg='white', font=('Times New Roman', 15), justify='left', borderwidth=5, width=10, command=lambda: self.send_message(user_entry, message_list))
        send_button.place(relx=0.8, rely=0.9, anchor='center')

        overwrite_button = tk.Button(root, text="Overwrite", bg='dark gray', fg='white', font=('Times New Roman', 15), justify='left', borderwidth=5, width=10, command=lambda: self.overwrite_button())
        overwrite_button.place(relx=0.8, rely=0.9, anchor='center')
        #######################################

        root.mainloop()

    def show_history_scrollbar(self, scrollbar):
        scrollbar.grid(row=0, column=1, sticky='ns')

    def show_message_scrollbar(self, scrollbar):
        scrollbar.grid(row=0, column=1, sticky='nsew')

    def hide_scrollbar(self, scrollbar):
        scrollbar.grid_forget()
    


if __name__ == "__main__":
    chatbot = ChatBot()
    chatbot.run()
