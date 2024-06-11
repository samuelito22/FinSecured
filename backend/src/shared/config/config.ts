import Joi from 'joi';
import dotenv from 'dotenv';
dotenv.config();

// Define the schema
const envVarsSchema = Joi.object({
    PORT: Joi.number().required(),
    NODE_ENV: Joi.string().valid('development', 'production', 'test').required(),
    DATABASE_URL: Joi.string().uri().required(),
    STRIPE_SECRET_KEY: Joi.string().required(),
    STRIPE_WEBHOOK_SECRET: Joi.string().required(),
    AUTH0_DOMAIN: Joi.string().uri().required(),
    AUTH0_API_AUDIENCE: Joi.string().uri().required()
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
        databaseUrl: validatedEnvVars.DATABASE_URL
    },
    stripe: {
        stripeSecretKey: validatedEnvVars.STRIPE_SECRET_KEY,
        stripeWebhookSecret: validatedEnvVars.STRIPE_WEBHOOK_SECRET
    },
    auth0: {
        auth0ApiAudience: validatedEnvVars.AUTH0_API_AUDIENCE,
        auth0Domain: validatedEnvVars.AUTH0_DOMAIN
    }
};