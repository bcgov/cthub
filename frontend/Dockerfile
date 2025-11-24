FROM node:16.13

WORKDIR /web

COPY package*.json /web/
RUN npm install --legacy-peer-deps

COPY . .

RUN mkdir -p /web/node_modules/.cache && chmod -R 777 /web/node_modules/.cache

EXPOSE 3000
