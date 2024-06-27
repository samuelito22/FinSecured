import { Request, Response } from "express";
import * as FeedbackServices from "../services/feedback.service"
import { CustomApiError, sendErrorResponse, sendSuccessResponse } from "@/shared/utils";

export const createUserFeedback = async (req: Request, res: Response) => {
    const { userId } = req.params
    const { content } = req.body

    try {
        await FeedbackServices.createUserFeedback({userId, content})
        sendSuccessResponse(res, 200, 'User feedback created successfully', { });
    } catch (error:any) {
        if (error instanceof CustomApiError) {
            sendErrorResponse(res, error.statusCode, error.message, error, 'UserFeedback');
        } else {
            console.error('Unexpected error:', error);
            sendErrorResponse(res, 500, 'Internal server error', error, 'UserFeedback');
        }
    }
}