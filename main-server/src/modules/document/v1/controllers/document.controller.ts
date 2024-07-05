import { Request, Response } from "express";
import { CustomApiError, sendErrorResponse, sendSuccessResponse } from "@/shared/utils";
import axios from "axios"
import { config } from "@/shared/config";

export const getAnswerToSearchQuery = async (req: Request, res: Response) => {
    const { query, regulation } = req.body;
    try {
        const response = await axios.post(`${config.aiApiUrl}/api/v1/documents/answer`, 
            { 
                query,
                regulation
            },
            {
                headers: {
                    'x-api-key': config.apiKey.finsecured, 
                    'Content-Type': 'application/json',
                }
            }
        );

        return sendSuccessResponse(res, 200, `Query successfully answered.`, { ...response.data.data });


    } catch (error:any) {
        if (error instanceof CustomApiError) {
            sendErrorResponse(res, error.statusCode, error.message, error, 'AnswerToQuery');
        } else {
            console.error('Unexpected error:', error);
            sendErrorResponse(res, 500, 'Internal server error', error, 'AnswerToQuery');
        }
    }
};

