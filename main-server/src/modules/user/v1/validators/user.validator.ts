import { NextFunction, Request, Response } from 'express';
import Joi from 'joi';

const userProfileSchema = Joi.object({
    userId: Joi.string().required(),
    email: Joi.string().email().required(),
    phoneNumber: Joi.string().regex(/^[0-9]{10}$/).required(),
    username: Joi.string().required()
});

export const validateUserProfile = (req:Request, res:Response, next:NextFunction) => {
    const { error } = userProfileSchema.validate(req.body);
    if (error) {
        return res.status(400).json({ error: error.details[0].message });
    }
    next();
};
