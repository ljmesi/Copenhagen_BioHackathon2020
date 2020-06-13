FROM python:buster
#as of the buster debian release, this driver works:
ARG URL="https://chromedriver.storage.googleapis.com/80.0.3987.106/chromedriver_linux64.zip"

WORKDIR /usr/src/app

COPY requirements.py ./

COPY . .

RUN cat /etc/apt/sources.list

RUN apt-get update -y

RUN apt-get install -y chromium

RUN echo $URL

RUN wget $URL;unzip chromedriver_linux64.zip

RUN pip3 install -r requirements.py

COPY /test_python/test_pycrawler.py .

CMD python3 -m unittest test_pycrawler.py

