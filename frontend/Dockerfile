# Fetching the latest node image on apline linux
FROM node:16.20-alpine AS builder

# Declaring env
ENV NODE_ENV development
ENV PORT=3000

# Setting up the work directory
WORKDIR /app

COPY package.json .
COPY package-lock.json .

RUN npm install

# Copying all the files in our project
COPY . .

# Building our application
RUN npm run build

EXPOSE $PORT

CMD ["npm", "run", "serverup"]
