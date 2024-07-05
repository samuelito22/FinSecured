# Build front-end
FROM node:20.13.1-bookworm-slim AS builder
WORKDIR /app
COPY package.json yarn.lock /app/
RUN yarn install --frozen-lockfile
COPY . /app

ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL}

RUN yarn build

# Production environment
FROM node:20.13.1-bookworm-slim
WORKDIR /app
COPY --from=builder /app/next.config.js /app
COPY --from=builder /app/public /app/public
COPY --from=builder /app/.next /app/.next
COPY --from=builder /app/node_modules /app/node_modules
COPY --from=builder /app/package.json /app


ENV PORT 3000
EXPOSE 3000

CMD ["yarn", "start"]
