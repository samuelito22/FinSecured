export interface IUser {
    id: string;
}

export interface IUserProfile {
    userId: string;
    email: string;
    phoneNumber: string;
    organization: string;
}

export interface CreateUserProps {
    userId: string;
    email: string;
    phoneNumber: string;
}

export interface CreateUserProfileProps {
    userId: string;
    organization: string;
}