FROM node:16.20.2

WORKDIR /usr/src/app

COPY package*.json ./

RUN npm install --legacy-peer-deps

COPY ./build ./build

CMD ["npx", "serve", "-s", "-l", "tcp://0.0.0.0:80", "build"]
