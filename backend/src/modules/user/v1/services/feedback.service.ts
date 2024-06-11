import { Transaction, ForeignKeyConstraintError } from 'sequelize';
import { Feedback } from '../models';
import { CustomApiError } from '../../../../shared/utils';
import { CreateUserFeedbackProps } from '../types';


export async function createUserFeedback({ userId, content }:CreateUserFeedbackProps, transaction?: Transaction): Promise<Feedback>{
    try {
        let feedback = await Feedback.create({
            userId,
            content
        }, {transaction})

        return feedback
    } catch (error) {
        if (error instanceof ForeignKeyConstraintError) {
            throw new CustomApiError(404, 'No such user exists to associate with feedback.');
        } else {
            throw error
        }
    }
}