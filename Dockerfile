FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential
RUN apt update && apt install -y libsm6 libxext6
RUN apt-get -y install tesseract-ocr

WORKDIR /app

COPY requirements.txt /app
RUN pip3 install -r requirements.txt

COPY src/ /app

CMD python3 app.py 9999