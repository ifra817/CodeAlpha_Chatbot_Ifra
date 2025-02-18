import json
import spacy
import random
import re
import wikipediaapi
import tkinter as tk
import textwrap
from tkinter import Canvas, scrolledtext

try:
    nlp = spacy.load("en_core_web_md")
except Exception as e:
    print("Error loading Spacy model:", e)
    exit()


def loadResponses():
    try:
        with open('responses.json') as file:
            return json.load(file)
    except FileNotFoundError:
        print("Error: responses.json file not found!")
        return {}

    
responses = loadResponses()

def preprocess_text(text):
    doc = nlp(text.lower())
    return " ".join([token.lemma_ for token in doc if not token.is_punct and not token.is_stop])

wiki = wikipediaapi.Wikipedia(user_agent="MyChatbot/1.0 (mailto:ifraahmed817@gmail.com)", language="en")
def get_wiki_summary(topic):
    topic = topic.strip()
    page = wiki.page(topic)
    if not page.exists() or not page.summary:
        return f"Sorry, I couldn't find information on '{topic}'."
    return page.summary[:500] + "..."

def math_operations(num1, operation, num2):
    if operation == "plus":
        return f"{num1} + {num2} = {num1 + num2}"
    elif operation == "minus":
        return f"{num1} - {num2} = {num1 - num2}"
    elif operation == "times":
        return f"{num1} × {num2} = {num1 * num2}"
    elif operation == "divided by" and num2 != 0:
        return f"{num1} ÷ {num2} = {num1 / num2:.2f}"
    return "I can't divide by zero!"


def get_response(user_input):
    clean_input = preprocess_text(user_input.lower())
    print(f"Clean input: {clean_input}")
    # Check if the user asks for a definition or summary
    match = re.search(r'(?:who|what) (is|was) (.+)', clean_input, re.IGNORECASE)
    if match:
        topic = clean_input
        print(f"Looking up topic: {topic}")
        return get_wiki_summary(topic)
    for pattern_data in responses.get("country_capitals", {}).get("patterns", []):
        match = re.search(pattern_data, user_input, re.IGNORECASE)
        if match:
            country = match.group(1).strip().lower()
            if country in responses["country_capitals"]["responses"]:
                return responses["country_capitals"]["responses"][country]
    # Check for general responses based on predefined patterns
    for category, data in responses.items():
        if category == "country_capitals" or category == "fallback":  # Skip to avoid rechecking capitals here
            continue
        for pattern in data["patterns"]:
            if re.search(rf"\b{pattern}\b", user_input, re.IGNORECASE):
                return random.choice(data["responses"])
    # Check for math operations like "what is 3 plus 2"
    match = re.search(r"what is (\d+) (plus|minus|times|divided by) (\d+)", user_input)
    if match:
        num1, operation, num2 = int(match.group(1)), match.group(2), int(match.group(3))
        return math_operations(num1, operation, num2)
    
    # If no matches, fall back to the default responses
    return random.choice(responses["fallback"]["responses"])


window = tk.Tk()

window.title("Chatbot")
window.geometry("800x600")

chat_canvas = Canvas(window, width=800, height=500, bg="white")
chat_canvas.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

bottom_frame = tk.Frame(window)
bottom_frame.pack(fill=tk.X, padx=10, pady=5)
   

def entry_focus(event):
    if user_entry.get() == "Message Chatbot":
        user_entry.delete(0, tk.END)
        user_entry.config(fg="black")

def entry_unfocus(event):
    if user_entry.get().strip() == "":
        user_entry.insert(0, "Message Chatbot")
        user_entry.config(fg="gray")

user_entry = tk.Entry(bottom_frame, fg="Gray", font=("Calibri", 12))
user_entry.insert(0, "Message Chatbot")
user_entry.bind("<FocusIn>", entry_focus)
user_entry.bind("<FocusOut>", entry_unfocus)
user_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5, ipadx=10, ipady=5)


def add_message(canvas, x1, y1, message, fill_color, text_color):
    message_lines = textwrap.wrap(message, width=50)  
    formatted_message = "\n".join(message_lines)

    text_id = canvas.create_text(x1 + 10, y1 + 10, text=formatted_message, fill=text_color, font=("Arial", 12), anchor="nw")
    bbox = canvas.bbox(text_id)
    
    if not bbox:
        return x1, y1

    text_width = bbox[2] - bbox[0] + 20
    text_height = bbox[3] - bbox[1] + 10

    x2 = x1 + text_width
    y2 = y1 + text_height

    canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline=fill_color)
    canvas.tag_raise(text_id)
    
    return x2, y2

def send_message(event=None):
    user_input = user_entry.get().strip()
    if not user_input or user_input == "Message Chatbot":
        return  

    last_items = chat_canvas.find_all()
    if last_items:
        last_bbox = chat_canvas.bbox(last_items[-1])
        y_position = last_bbox[3] + 20 if last_bbox else 10
    else:
        y_position = 10  

    user_x1 = max(800 - len(user_input) * 7 - 60, 450)
    _, user_y2 = add_message(chat_canvas, user_x1, y_position, user_input, "#E5E5EA", "black")

    response = get_response(user_input)

    bot_x1 = 50
    _, bot_y2 = add_message(chat_canvas, bot_x1, user_y2 + 10, response, "blue", "white")

    chat_canvas.config(scrollregion=chat_canvas.bbox("all"))

    user_entry.delete(0, tk.END)
    user_entry.config(fg="black")



send_button = tk.Button(bottom_frame, text="Send",fg="blue", command=send_message)
send_button.pack(side=tk.RIGHT, padx=5, ipadx=10, ipady=5)
user_entry.pack_configure(ipady=5)
user_entry.bind("<Return>", send_message)

window.mainloop()

