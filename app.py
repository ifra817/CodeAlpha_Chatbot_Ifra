
import json
import spacy
import random
import re
import wikipediaapi
import tkinter as tk
import textwrap
import math
from tkinter import Canvas, scrolledtext
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os


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
    processed_text = [token.lemma_ if token.lemma_ != "-PRON-" else token.text for token in doc if not token.is_punct and not token.is_stop]
    return " ".join(processed_text)

wiki = wikipediaapi.Wikipedia(user_agent="MyChatbot/1.0 (mailto:ifraahmed817@gmail.com)", language="en")

def get_wiki_summary(topic):
    try:
        # Fetch the page
        page = wiki.page(topic)    
        # Check if the page exists
        if not page.exists():
            return "Sorry, I couldn't find anything on that topic."
        return page.summary[:500]  # You can adjust this length as needed
    except wikipediaapi.exceptions.DisambiguationError as e:
        # If disambiguation happens, provide a list of options
        return f"Your query is ambiguous. Did you mean: {', '.join(e.options[:5])}?"
    except wikipediaapi.exceptions.PageError:
        return "Sorry, I couldn't find anything on that topic."
    except Exception as e:
        return f"Sorry, I couldn't fetch information due to an error: {str(e)}"


def math_operations(num1, operation, num2=None):
    operations = {
        "plus": lambda x, y: x + y,
        "minus": lambda x, y: x - y,
        "times": lambda x, y: x * y,
        "divided by": lambda x, y: x / y if y != 0 else "I can't divide by zero!",
        "power": lambda x, y: x ** y,
        "modulus": lambda x, y: x % y,
        "sqrt": lambda x, _: math.sqrt(x) if x >= 0 else "I can't calculate square root of negative numbers!"
    }
    return f"{num1} {operation} {num2 if num2 is not None else ''} = {operations.get(operation, lambda x, y: 'Invalid')(num1, num2)}"
  


def extract_query(text):
    sqrt_match = re.search(r"what is sqrt (\d+\.?\d*)", text, re.IGNORECASE)
    if sqrt_match:
        return math_operations(float(sqrt_match.group(1)), "sqrt")   
    math_match = re.search(r'what is (\d+\.?\d*) (plus|minus|times|divided by|power|modulus) (\d+\.?\d*)', text, re.IGNORECASE)
    if math_match:
        return math_operations(float(math_match.group(1)), math_match.group(2), float(math_match.group(3)))

    # Wikipedia query
    wiki_match = re.search(r'who is (.+)|tell me about (.+)', text, re.IGNORECASE)
    if wiki_match:
        topic = wiki_match.group(1) if wiki_match.group(1) else wiki_match.group(2)
        return get_wiki_summary(topic)
    return None


context = {}
def get_response(user_input):
    global context
    clean_input = preprocess_text(user_input.lower())
    print(f"Clean input: {clean_input}")
    
    # Check for Wikipedia queries first
    extracted_response = extract_query(user_input)
    if extracted_response:
        print(extracted_response)
        return extracted_response 

    # Handle name-related queries
    if "my name is" in user_input.lower():
        name = user_input.lower().split("my name is")[-1].strip().capitalize()
        context["user_name"] = name
        return f"Nice to meet you, {name}!"
    elif "what is my name" in user_input:
        if "user_name" in context:
            return f"Your name is {context['user_name']}!"
        else:
            return "I don't know your name yet. Tell me!"

    # Check for country capitals
    for pattern_data in responses.get("country_capitals", {}).get("patterns", []):
        match = re.search(pattern_data, user_input, re.IGNORECASE)
        if match:
            country = match.group(1).strip().lower()
            if country in responses["country_capitals"]["responses"]:
                return responses["country_capitals"]["responses"][country]

    # Check for general responses based on predefined patterns
    for category, data in responses.items():
        if category in ["country_capitals", "fallback", "wikipedia_queries"]:
            continue
        for pattern in data["patterns"]:
            if re.search(rf"\b{pattern}\b", user_input, re.IGNORECASE):
                return random.choice(data["responses"])

    # Log unknown queries
    if not extracted_response and not context.get("user_name"):
        unknown_file_path = os.path.join(os.getcwd(), "unknown_queries.txt")
        try:
            with open("unknown_queries.txt", "a") as f:
                f.write(user_input + "\n")
        except Exception as e:
            print(f"Error writing to unknown_queries.txt: {e}")

    return random.choice(responses["fallback"]["responses"])




window = tk.Tk()
window.title("Chatbot")
window.geometry("800x600")

chat_frame = tk.Frame(window)
chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

chat_scrollbar = tk.Scrollbar(chat_frame)
chat_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

chat_canvas = Canvas(chat_frame, width=800, height=500, bg="white", yscrollcommand=chat_scrollbar.set)
chat_canvas.pack(fill=tk.BOTH, expand=True)

chat_scrollbar.config(command=chat_canvas.yview)

bottom_frame = tk.Frame(window)
bottom_frame.pack(fill=tk.X, padx=10, pady=5)
   

def entry_focus(event):
    if user_entry.get() == "Message Chatbot":
        user_entry.delete(0, tk.END)
        user_entry.config(fg="black")

def entry_unfocus(event):
    if not user_entry.get():
        user_entry.insert(0, "Message Chatbot")
        user_entry.config(fg="gray")

user_entry = tk.Entry(bottom_frame, fg="black", font=("Calibri", 12))
user_entry.insert(0, "Message Chatbot")
user_entry.bind("<FocusIn>", entry_focus)
user_entry.bind("<FocusOut>", entry_unfocus)
user_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5, ipadx=10, ipady=5)


def add_message(canvas, x1, y1, message, fill_color, text_color):
    message_lines = textwrap.wrap(message, width=60)  
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

