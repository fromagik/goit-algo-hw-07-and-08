
FROM python:3.12.4

RUN apt-get update && \
    apt-get install -y python3-tk && \
    apt-get install -y x11-apps && \
    apt-get clean
    
WORKDIR /app

COPY . /app

CMD ["python", "app.py"]

