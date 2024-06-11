import { CustomApiError } from "../../../../shared/utils";
import { Subscription } from "../models";
import { ForeignKeyConstraintError, Transaction } from "sequelize";
import { CreateSubscriptionProps, CreateFullSubscriptionProps } from "../types";

export async function createSubscription(props: CreateSubscriptionProps, transaction?: Transaction): Promise<Subscription> {
    const { isTrial, startDate, endDate, userId } = props;

    try {
        // Check if a subscription already exists for the user
        const existingSubscription = await Subscription.findOne({ where: { userId }, transaction });
        if (existingSubscription) {
            throw new CustomApiError(409, 'Subscription with this user ID already exists.');
        }

        // Create subscription based on trial or full subscription specifics
        if (!isTrial) {
            // Ensure props are of the type CreateFullSubscriptionProps for TypeScript safety
            const fullProps = props as CreateFullSubscriptionProps;
            const { planId, stripeSubscriptionId } = fullProps;
            const subscription = await Subscription.create({
                isTrial,
                startDate,
                endDate,
                userId,
                planId,
                stripeSubscriptionId,
                status: 'active'  // Assuming initial status for new full subscriptions
            }, { transaction });
            return subscription;
        } else {
            // For trial, planId and stripeSubscriptionId should be null and handled by model validation
            const subscription = await Subscription.create({
                isTrial,
                startDate,
                endDate,
                userId,
                status: 'trial'  // Assuming initial status for new trial subscriptions
            }, { transaction });
            return subscription;
        }
    } catch (error) {
        if (error instanceof ForeignKeyConstraintError) {
            throw new CustomApiError(404, 'No such user exists to associate with a subscription.');
        } else {
            throw error;
        }
    }
}
