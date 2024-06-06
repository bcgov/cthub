FROM node:16.13

WORKDIR /web

COPY package*.json /web/
RUN npm install --legacy-peer-deps

COPY . .

EXPOSE 3000
