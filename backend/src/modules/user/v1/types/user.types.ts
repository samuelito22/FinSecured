export interface IUser {
    id: string;
    // Add other necessary user properties
}

export interface IUserProfile {
    userId: string;
    email: string;
    phoneNumber: string;
    organization: string;
    // Add other necessary user profile properties
}

export interface CreateUserProfileProps {
    userId: string;
    email: string;
    phoneNumber: string;
    organization: string;
}