import express from 'express';
import jwks from 'jwks-rsa';
import { expressjwt as jwt, Params } from "express-jwt";
import { config } from '../config';

const authCheck = jwt({
    secret: jwks.expressJwtSecret({
        cache: true,
        rateLimit: true,
        jwksRequestsPerMinute: 5,
        jwksUri: config.auth0.auth0Domain,
    }),
    audience: config.auth0.auth0ApiAudience,
    issuer: config.auth0.auth0Domain,
    algorithms: ['RS256'] 
} as Params);

export default authCheck;
