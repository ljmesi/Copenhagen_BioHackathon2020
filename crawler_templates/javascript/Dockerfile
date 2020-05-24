FROM browserless/base:latest

WORKDIR /usr/src/app

COPY package*.json ./

RUN npm install

COPY ./start.sh /

COPY . .

RUN chmod 755 /start.sh

ENTRYPOINT ["sh", "start.sh"]
