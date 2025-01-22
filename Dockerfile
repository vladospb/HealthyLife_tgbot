FROM python:3.12.4

WORKDIR /app

COPY requirements.txt requirements.txt
COPY bot.py bot.py
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "bot.py"]