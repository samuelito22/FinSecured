export interface IFeedback {
    id: string;
    userId: string;
    content:string;
}

export interface CreateUserFeedbackProps {
    userId: string;
    content: string;
}