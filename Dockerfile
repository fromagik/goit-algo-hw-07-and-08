FROM python:3.12.4-slim

WORKDIR /app

COPY . /app

CMD ["python", "bot.py"]
