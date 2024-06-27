import Joi from "joi";
import { Request, Response, NextFunction } from "express";

enum Regulation {
    FCA = "FCA",
}

const getAnswerToSearchQuerySchema = Joi.object({
    query: Joi.string().required(),
    regulation: Joi.string().valid(...Object.values(Regulation)).required(),
});

export const validateGetAnswerToSearchQuery = (req: Request, res: Response, next: NextFunction) => {
    const { error } = getAnswerToSearchQuerySchema.validate(req.body);
    if (error) {
        return res.status(400).json({ error: error.details[0].message });
    }
    next();
};
