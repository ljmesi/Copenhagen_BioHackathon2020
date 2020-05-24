FROM browserless/base:latest

WORKDIR /usr/src/app

COPY . .

RUN apt-get update -y

RUN apt-get install -y maven openjdk-11-jre openjdk-11-jdk

COPY ./start.sh /

RUN chmod 755 /start.sh

ENTRYPOINT ["sh", "start.sh"]
