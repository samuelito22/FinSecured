# Stage 1: Build
FROM node:20.13.1-alpine as builder

# Set working directory
WORKDIR /opt/app

# Install dependencies
COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile

# Copy the rest of the application code
COPY . .

# Build the application
RUN yarn build

# Stage 2: Production Environment
FROM node:20.13.1-alpine as production

# Set working directory
WORKDIR /opt/app

# Only copy over the built artifacts and necessary files
COPY --from=builder /opt/app/dist ./dist
COPY package.json yarn.lock ./

# Install only production dependencies
RUN yarn install --production

# Environment Variables
ARG NODE_ENV
ARG CORS_ORIGIN
ARG MAIN_DATABASE_URL
ARG STRIPE_SECRET_KEY
ARG STRIPE_WEBHOOK_SECRET
ARG AUTH0_DOMAIN
ARG AUTH0_API_AUDIENCE
ARG FINSECURED_API_KEY
ARG PORT
ARG AI_API_URL

ENV NODE_ENV=${NODE_ENV} \
    CORS_ORIGIN=${CORS_ORIGIN} \
    MAIN_DATABASE_URL=${MAIN_DATABASE_URL} \
    STRIPE_SECRET_KEY=${STRIPE_SECRET_KEY} \
    STRIPE_WEBHOOK_SECRET=${STRIPE_WEBHOOK_SECRET} \
    AUTH0_DOMAIN=${AUTH0_DOMAIN} \
    AUTH0_API_AUDIENCE=${AUTH0_API_AUDIENCE} \
    FINSECURED_API_KEY=${FINSECURED_API_KEY} \
    PORT=${PORT} \
    AI_API_URL=${AI_API_URL}

# Expose port and define command
EXPOSE ${PORT}
CMD ["node", "dist/index.js"]
