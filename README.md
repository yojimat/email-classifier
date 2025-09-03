# AI Email Classification System

An intelligent AI-powered system for classifying emails and generating automatic responses.

## 🚀 Features

- **Smart Email Classification** → Sorts emails into Productive or Unproductive
- **AI-Powered Auto-Responses** → Generates contextual replies instantly
- **Multi-Format Support** → Works with .txt and .pdf files
- **NLP Under the Hood** → Powered by NLTK + Transformers
- **RESTful API** → Scalable backend built with Flask

## 📋 Requirements

- Python 3.12+
- Minimum 4GB RAM
- 2GB free disk space (for models)

## 🔧 Installation

All the commands must be made inside the `api` directory.

### 1. Clone the repo

```bash
git clone https://github.com/seu-usuario/email-classifier-ai.git
cd email-classifier-ai
```

### 2. Create a virtual environment

```bash
python -m venv ".venv"
source .venv/bin/activate  # No Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

```bash
cp .env.example .env
# Edit .env with your API keys
```

### 5. Download NLTK resources

```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet');nltk.download('punkt_tab');"
```

## 🏃 Running the Project

### Backend

```bash
cd api
python app.py
```

👉 Available at: `http://localhost:5000`

### Frontend

Open index.html in your browser or run a simple HTTP server:

```bash
cd web
python -m http.server 8000
```

👉 Visit: `http://localhost:8000`

# 📚 API Documentation

TODO: Try to create a swagger documentation

## 🔬 Tech Stack

### Backend

- **Flask**: Web framework
- **NLTK**: Natural Language Processing
- **Transformers**: Pre-trained AI models
- **PyPDF2**: PDF file parsing
- **OpenAI API**: Advanced response generation (optional)

### Frontend

- **HTML5/CSS3**: Structure and styling
- **JavaScript**: Interactivity
- **Reponsive Design**: Mobile-first
- **CSS Animations**: Visual feedback

## 🛠️ Customization

### Add Keywords

Edit `PRODUCTIVE_KEYWORDS` e `UNPRODUCTIVE_KEYWORDS` em `app.py`.

### Switch Models

Update `CLASSIFICATION_MODEL` na classe `Config`.

### Custom Response Templates

Edit the templates in `_generate_template_response()`.

## Future Updates

- When the 2 inputs are filled, ask the user which one they want to use
- Create a Subject input for when the user send a text
- Verify if the Customization readme part is still truth
- See about the Swagger documentation for the API
