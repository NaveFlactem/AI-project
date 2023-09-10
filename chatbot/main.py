import json
import tkinter as tk
from tkinter import simpledialog
from tkinter import font
from difflib import get_close_matches

def load_knowledge_base(file_path: str) -> dict:
    with open('knowledge_base.json', 'r') as f:
        knowledge_base = json.load(f)
    return knowledge_base

def save_knowledge_base(file_path: str, knowledge_base: dict) -> None:
    with open('knowledge_base.json', 'w') as f:
        json.dump(knowledge_base, f, indent=2)

def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q['question'] == question:
            return q['answer']

def collect_user_input(user_input):
    user_response = simpledialog.askstring("User Input", user_input)
    return user_response

def update_chat(user_input, chat_text, user_entry):
    user_message = f"User: {user_input}\n"
    chat_text.config(state=tk.NORMAL)
    chat_text.insert(tk.END, user_message)
    chat_text.config(state=tk.DISABLED)

    best_match: str | None = find_best_match(user_input, [q['question'] for q in knowledge_base["questions"]])

    if best_match:
        answer: str = get_answer_for_question(best_match, knowledge_base)
        response = f"Bot: {answer}\n"
    else:
        response = "Bot: Sorry, I don't know what to say. Can you teach me?\n"
        chat_text.config(state=tk.NORMAL)
        chat_text.insert(tk.END, response)
        chat_text.config(state=tk.DISABLED)
        
        response = "\nType answer to your prompt or type 'skip' to skip: "
        chat_text.config(state=tk.NORMAL)
        chat_text.insert(tk.END, response)
        chat_text.config(state=tk.DISABLED)
        
        new_answer: str = collect_user_input(response)

        if new_answer and new_answer.lower() != 'skip':
            knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
            save_knowledge_base('knowledge_base.json', knowledge_base)
            response = "\nBot: Thanks, I'll remember that.\n"
        else:
            response = "\nBot: Okay, I'll skip.\n"

    chat_text.config(state=tk.NORMAL)
    chat_text.insert(tk.END, response)
    chat_text.config(state=tk.DISABLED)
    user_entry.delete(0, tk.END)

def send_message(event):
    user_input = user_entry.get()
    if user_input.lower() == 'exit':
        root.quit()
    update_chat(user_input, chat_text, user_entry)

if __name__ == "__main__":
    knowledge_base: dict = load_knowledge_base('knowledge_base.json')

    root = tk.Tk()
    root.title("Chat Bot")

    initial_width = 800
    initial_height = 600

    root.geometry(f"{initial_width}x{initial_height}")

    chat_text = tk.Text(root, state=tk.DISABLED)
    chat_text.pack()

    user_entry = tk.Entry(root)
    user_entry.pack()
    user_entry.bind("<Return>", send_message)

    root.mainloop()
