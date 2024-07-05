# Stage 1: Build the application
FROM node:alpine as builder

# Set the working directory
WORKDIR /opt/app

# Copy package.json and yarn.lock files
COPY package.json yarn.lock ./

# Install all dependencies
RUN yarn install --frozen-lockfile

# Copy the rest of the application
COPY . .

# Build the application
RUN yarn build

# Stage 2: Setup the production environment
FROM node:alpine

# Set the working directory
WORKDIR /opt/app

# Copy package.json and yarn.lock files
COPY package.json yarn.lock ./

# Install only production dependencies
RUN yarn install --frozen-lockfile --production

# Copy built assets from the builder stage
COPY --from=builder /opt/app/dist ./dist

# Setup environment variables
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

# Expose the application port
EXPOSE ${PORT}

# Command to run the application
CMD ["node", "dist/index.js"]
