import { Response } from 'express';

interface ErrorResponseDetail {
    context: string;
    codes: { [key: string]: string[] };
    messages: { [key: string]: string[] };
}

interface CustomError extends Error {
    errors?: Array<{
        message: string;
        type: string;
        path: string;
    }>;
}

export function sendErrorResponse(res: Response, statusCode: number, message: string, error: CustomError, context: string): void {
    const response: any = {
        error: {
            name: error.name || 'Error',
            status: statusCode,
            message,
            statusCode,
            details: {
                context,
                codes: {},
                messages: {}
            } as ErrorResponseDetail
        }
    };

    if (process.env.NODE_ENV !== 'production') {
        response.error.stack = error.stack; // Include stack trace only in non-production environments
    }

    if (error.errors) {
        error.errors.forEach(err => {
            response.error.details.codes[err.path] = [err.type];
            response.error.details.messages[err.path] = [err.message];
        });
    }

    res.status(statusCode).json(response);
}

export function sendSuccessResponse<T>(res: Response, statusCode: number, message: string, data: T): void {
    const response = {
        message,
        success: true,
        data
    };

    res.status(statusCode).json(response);
}

export class CustomApiError extends Error {
    statusCode: number;
    name: string;

    constructor(statusCode: number, message: string) {
        super(message); // Pass the message to the parent Error class
        this.statusCode = statusCode;
        this.name = 'CustomApiError'; // Overriding the name property to identify this error
        Object.setPrototypeOf(this, CustomApiError.prototype); // Restore prototype chain
    }
}
