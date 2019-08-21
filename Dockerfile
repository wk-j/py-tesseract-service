FROM ubuntu:19.10
RUN apt-get -y update
RUN apt-get -y install python3-pip python3-dev build-essential
RUN apt-get -y install libsm6 libxext6
RUN apt-get -y install tesseract-ocr

WORKDIR /app

COPY requirements.txt /app
RUN pip3 install -r requirements.txt

COPY src/ /app

CMD python3 app.py 9999