import { User, UserProfile } from '../models';
import sequelize from '../../../../shared/db/sequelize';
import { IUser, IUserProfile, IUserProfileData, IUserProfileResponse } from '../types';

async function createUserIfNotExists(userId:string): Promise<IUser> {
    let user = await User.findByPk(userId);
    if (!user) {
        user = await User.create({ id: userId });
    }
    return user;
}

async function createUserProfile({ userId, email, phoneNumber, organization }: IUserProfileData): Promise<IUserProfileResponse> {
    const t = await sequelize.transaction();
    try {
        const user = await createUserIfNotExists(userId);
        let userProfile = await UserProfile.findOne({ where: { userId } });
        if (userProfile) {
            userProfile = await userProfile.update({ email, phoneNumber, organization });
        } else {
            userProfile = await UserProfile.create({ userId, email, phoneNumber, organization });
        }
        await t.commit();
        return { user, userProfile };
    } catch (error) {
        await t.rollback();
        throw error;
    }
}

export { createUserProfile };