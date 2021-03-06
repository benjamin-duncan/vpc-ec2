FROM node:latest

WORKDIR /frontend

COPY package.json package-lock.json /frontend/

RUN npm install

CMD ["npm","run","serve"]