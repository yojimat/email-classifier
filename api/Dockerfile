FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('averaged_perceptron_tagger'); nltk.download('punkt_tab');"

COPY . .

RUN mkdir -p models

EXPOSE 8080

CMD ["gunicorn", "--config", "gunicorn_config.py", "app:app"]
