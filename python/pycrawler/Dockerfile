#FROM python:buster
FROM browserless/base:latest
#as of the buster debian release, this driver works:
#ARG URL="https://chromedriver.storage.googleapis.com/80.0.3987.106/chromedriver_linux64.zip"

WORKDIR /usr/src/app

COPY requirements.py ./

#RUN echo "deb http://ftp.nl.debian.org/debian-security stable/updates/main amd64 Packages" > /etc/apt/sources.list
#RUN echo "deb-src http://ftp.nl.debian.org/debian-security stable/updates/main amd64 Packages" >> /etc/apt/sources.list
#RUN cat /etc/apt/sources.list

RUN apt-get update -y

RUN apt-get install -y python3 python3-pip

#RUN echo $URL

#RUN wget $URL;unzip chromedriver_linux64.zip
RUN pip3 install -r requirements.py

COPY ./start.sh /

COPY . .

RUN chmod 755 /start.sh

ENTRYPOINT ["sh", "start.sh"]
