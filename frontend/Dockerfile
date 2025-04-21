FROM node:20-alpine AS builder
WORKDIR /app

COPY package*.json ./
RUN yarn

COPY . .
RUN yarn build

FROM nginx:stable-alpine

COPY --from=builder /app/dist /usr/share/nginx/html

RUN rm /etc/nginx/conf.d/default.conf
COPY /nginx/default.conf /etc/nginx/conf.d

CMD ["nginx", "-g", "daemon off;"]