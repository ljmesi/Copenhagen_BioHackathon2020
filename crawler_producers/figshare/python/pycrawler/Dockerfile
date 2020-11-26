FROM python:buster
#as of the buster debian release, this driver works:
#result of `apt-get search chromium`
#chromium/stable,stable 83.0.4103.116-1~deb10u3 amd64
#  web browser
ARG URL="https://chromedriver.storage.googleapis.com/83.0.4103.39/chromedriver_linux64.zip"

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN cat /etc/apt/sources.list

RUN apt-get update -y

RUN apt-get install -y chromium

RUN echo $URL

RUN wget $URL;unzip chromedriver_linux64.zip

RUN pip3 install -r requirements.txt

COPY ./start.sh /

COPY . .

RUN chmod 755 /start.sh

ENTRYPOINT ["sh", "start.sh"]
