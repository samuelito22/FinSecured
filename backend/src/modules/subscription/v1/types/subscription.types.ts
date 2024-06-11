interface BaseSubscriptionProps {
    isTrial: boolean;
    userId: string;
    startDate: Date;
    endDate: Date;
  }

export interface CreateTrialSubscriptionProps extends BaseSubscriptionProps {
    isTrial: true;
}

export interface CreateFullSubscriptionProps extends BaseSubscriptionProps {
    isTrial: false;
    planId: number;
    stripeSubscriptionId: string;
}
  

export type CreateSubscriptionProps = CreateFullSubscriptionProps | CreateTrialSubscriptionProps