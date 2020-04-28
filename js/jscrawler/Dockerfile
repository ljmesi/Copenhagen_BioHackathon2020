#FROM node:12
FROM browserless/base:latest

WORKDIR /usr/src/app

COPY package*.json ./

RUN npm install

COPY . .

CMD [ "node", "crawler.js" ]
