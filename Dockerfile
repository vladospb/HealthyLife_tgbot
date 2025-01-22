FROM python:3.12.4

WORKDIR /app

COPY .venv/requirements.txt .venv/requirements.txt
COPY bot.py bot.py
RUN pip install -r .venv/requirements.txt

COPY . .

CMD ["python", "bot.py"]