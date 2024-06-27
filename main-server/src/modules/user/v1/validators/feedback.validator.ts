import { NextFunction, Request, Response } from 'express';
import Joi from 'joi';

const userFeedbackSchema = Joi.object({
    userId: Joi.string().required(),
    content: Joi.string().required()
});

export const validateUserFeedback = (req:Request, res:Response, next:NextFunction) => {
    const { error } = userFeedbackSchema.validate(req.body);
    if (error) {
        return res.status(400).json({ error: error.details[0].message });
    }
    next();
};
