import { Request, Response } from 'express';
import sequelize from '@/shared/db/sequelize.config';
import { createUserIfNotExists, createUserProfile } from '../services';
import { CustomApiError, sendErrorResponse, sendSuccessResponse } from '@/shared/utils';
import { createSubscription } from '@/modules/subscription/v1/services';

export const createUser = async (req: Request, res: Response) => {
    const { userId, email, phoneNumber, organization } = req.body;

    const t = await sequelize.transaction();

    try {
        const user = await createUserIfNotExists({userId, email, phoneNumber}, t);
        const userProfile = await createUserProfile({ userId, organization}, t);     
        await createSubscription({
            userId: user.id, 
            isTrial: true, 
            startDate: new Date, 
            endDate: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000)
        })

        await t.commit();
        sendSuccessResponse(res, 200, 'User profile created successfully', { user, userProfile });
    } catch (error:any) {
        await t.rollback();  
        
        if (error instanceof CustomApiError) {
            sendErrorResponse(res, error.statusCode, error.message, error, 'UserProfile');
        } else {
            console.error('Unexpected error:', error);
            sendErrorResponse(res, 500, 'Internal server error', error, 'UserProfile');
        }
    }
}