# Chatbot

An interactive AI-powered chatbot built with Python, designed to engage in conversations, answer general questions, perform simple math operations, fetch Wikipedia summaries, and log unknown queries for future improvements. It also features a user-friendly GUI built with Tkinter.

## ✨ Features

- **Natural Language Processing** with SpaCy for input preprocessing.
- **Wikipedia Integration** using `wikipediaapi` to fetch summaries.
- **Simple Math Operations** like addition, subtraction, multiplication, division, powers, modulus, and square roots.
- **Country Capitals** response from predefined data.
- **Context Awareness** for user-specific queries (e.g., remembering names).
- **GUI Interface** built with Tkinter for interactive chat.
- **Unknown Query Logging** in `unknown_queries.txt` for future enhancements.

## 🛠 Technologies Used

- **Python 3**
- **Visual Studio Code**
- **SpaCy** (`en_core_web_md` model) for NLP
- **Wikipedia-API** for fetching article summaries
- **Tkinter** for GUI
- **scikit-learn** and **numpy** for cosine similarity
- **JSON** for storing predefined responses
- **textwrap**, **re**, **math**, and **os** for text handling and system operations

## 📁 Project Structure

```plaintext
Chatbot/
│
├── app.py           # Main chatbot logic and GUI
├── responses.json       # Predefined chatbot responses
├── unknown_queries.txt  # Logs unknown user queries
├── requirements.txt     # Dependencies
└── README.md            # Project documentation
```

## ⚡ Installation

### Clone the Repository

```bash
git clone https://github.com/ifra817/CodeAlpha_Chatbot_Ifra.git
cd CodeAlpha_Chatbot_Ifra
```
### Set Up Virtual Environment
```bash
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
Note: The virtual environment folder (venv/) has been excluded from the repository. Use the provided requirements.txt to install dependencies.
```
### Install Dependencies

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_md
```

## 🚀 Usage

Run the chatbot with:

```bash
python app.py
```

### 📌 Future Enhancements
- Advanced NLP capabilities for better understanding and context.
- More API Integrations (e.g., weather, news).
- Voice Interaction Support using speech recognition.
- Improved GUI with themes and user settings.
- Machine Learning for dynamic response generation.


