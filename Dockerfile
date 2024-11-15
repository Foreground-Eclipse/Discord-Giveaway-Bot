
FROM python:3.9-slim

WORKDIR /giveawaysbot

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]