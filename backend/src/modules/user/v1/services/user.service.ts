import { CustomApiError } from '../../../../shared/utils';
import { User, UserProfile } from '../models';
import { CreateUserProfileProps, IUser } from '../types';
import { Transaction, ForeignKeyConstraintError } from 'sequelize';

async function createUserIfNotExists(userId:string, transaction?: Transaction): Promise<IUser> {
    try {
        let user = await User.findByPk(userId);
        if (user) throw new CustomApiError(409, 'User with this ID already exists.');

        user = await User.create({ id: userId }, { transaction }); 
        return user;
    } catch (error){
        throw error
    }
}

async function createUserProfile({ userId, email, phoneNumber, organization }: CreateUserProfileProps, transaction?: Transaction): Promise<UserProfile> {
    try {
        let userProfile = await UserProfile.findOne({ where: { userId } });
        if (userProfile) {
            userProfile = await userProfile.update({ email, phoneNumber, organization }, {transaction});
        } else {
            userProfile = await UserProfile.create({ userId, email, phoneNumber, organization }, {transaction});
        }
        return userProfile;
    } catch (error) {
        if (error instanceof ForeignKeyConstraintError) {
            throw new CustomApiError(404, 'No such user exists to associate with profile.');
        } else {
            throw error
        }
    }
}

export { createUserIfNotExists, createUserProfile };