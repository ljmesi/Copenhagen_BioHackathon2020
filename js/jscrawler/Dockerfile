#FROM node:12
FROM browserless/base:latest

WORKDIR /usr/src/app

COPY package*.json ./

RUN npm install

COPY ./start.sh /

COPY . .

RUN chmod 755 /start.sh

#CMD [ "node", "crawler.js" ]
ENTRYPOINT ["sh", "start.sh"]
