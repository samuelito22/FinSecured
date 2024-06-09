import express from 'express';
import jwks from 'jwks-rsa';
import { expressjwt as jwt, Params } from "express-jwt";


const authCheck = jwt({
    secret: jwks.expressJwtSecret({
        cache: true,
        rateLimit: true,
        jwksRequestsPerMinute: 5,
        jwksUri: `https://your-auth0-domain/.well-known/jwks.json`,
    }),
    audience: 'your-api-audience',
    issuer: `https://your-auth0-domain/`,
    algorithms: ['RS256'] 
} as Params);

export default authCheck;
