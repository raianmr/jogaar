FROM node:18.9

WORKDIR /usr/src/web

COPY package*.json ./

RUN npm install --silent

COPY . .

CMD npm start
