FROM node:20.13.1-bookworm-slim

WORKDIR /opt/app

ENV NODE_ENV production

COPY package.json yarn.lock ./

RUN yarn install --frozen-lockfile

COPY . /opt/app

ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL}

RUN yarn install --production=false && yarn build

EXPOSE 3000

CMD [ "yarn", "start" ]
