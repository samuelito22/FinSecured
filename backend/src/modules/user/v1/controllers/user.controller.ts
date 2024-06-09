import { Request, Response } from 'express';
import { User, UserProfile } from '../models';
import sequelize from '../../../../shared/db/sequelize';

export const createUserProfile = async (req: Request, res: Response) => {
    const { userId, email, phoneNumber, organization } = req.body;

    const t = await sequelize.transaction();

    try {
        // Ensure the user exists
        let user = await User.findByPk(userId);
        if (!user) {
            // Create the user if not existing
            user = await User.create({ id: userId });
        }

        // Check if user profile already exists
        let userProfile = await UserProfile.findOne({ where: { userId } });
        if (userProfile) {
            // Update existing profile
            userProfile = await userProfile.update({ email, phoneNumber, organization });
        } else {
            // Create new profile
            userProfile = await UserProfile.create({ userId, email, phoneNumber, organization });
        }

        await t.commit();
        res.status(200).json({ user, userProfile });
    } catch (error:any) {
        await t.rollback();  
        
        console.error('Error managing user data:', error);
        
        switch (error.name) {
            case 'SequelizeUniqueConstraintError':
                res.status(409).send('Conflict: The data provided conflicts with existing data.');
                break;
            case 'SequelizeValidationError':
                res.status(400).send('Validation error: Data is not in the expected format.');
                break;
            default:
                // General error handling for other types of errors
                res.status(500).send('Failed to manage user data.');
                break;
        }
    }
}