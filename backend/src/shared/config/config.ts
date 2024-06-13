import Joi from 'joi';
import dotenv from 'dotenv';
import Stripe from 'stripe';
dotenv.config();

// Define the schema
const envVarsSchema = Joi.object({
    PORT: Joi.number().required(),
    NODE_ENV: Joi.string().valid('development', 'production', 'test').required(),
    MAIN_DATABASE_URL: Joi.string().uri().required(),
    EMBEDDING_DATABASE_URL: Joi.string().uri().required(),
    STRIPE_SECRET_KEY: Joi.string().required(),
    STRIPE_WEBHOOK_SECRET: Joi.string().required(),
    AUTH0_DOMAIN: Joi.string().uri().required(),
    AUTH0_API_AUDIENCE: Joi.string().uri().required(),
    MISTRAL_AI_API_KEY: Joi.string().required()
}).unknown(true);  // Allows for other non-specified env variables

// Validate the environment variables
const { value: validatedEnvVars, error } = envVarsSchema.prefs({ errors: { label: 'key' } }).validate(process.env);

if (error) {
  throw new Error(`Config validation error: ${error.message}`);
}

console.log('All required configurations are present.');

// Export validated PORT environment variable
export const config = {
    port: validatedEnvVars.PORT,
    env: validatedEnvVars.NODE_ENV,
    database: {
        mainDatabaseUrl: validatedEnvVars.MAIN_DATABASE_URL,
        embeddingDatabaseUrl: validatedEnvVars.EMBEDDING_DATABASE_URL
    },
    stripe: {
        stripeSecretKey: validatedEnvVars.STRIPE_SECRET_KEY,
        stripeWebhookSecret: validatedEnvVars.STRIPE_WEBHOOK_SECRET
    },
    auth0: {
        auth0ApiAudience: validatedEnvVars.AUTH0_API_AUDIENCE,
        auth0Domain: validatedEnvVars.AUTH0_DOMAIN
    },
    mistral_ai:{
        apiKey: validatedEnvVars.MISTRAL_AI_API_KEY
    }
};

export const stripe = new Stripe(config.stripe.stripeSecretKey)