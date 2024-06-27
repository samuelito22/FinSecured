import { Request, Response } from 'express';
import Stripe from 'stripe';
import { config, stripe } from '../../../../shared/config';
import { Plan, Subscription } from '../models';
import * as StripeServices from "../services/stripe.service"
import { User } from '../../../user/v1/models';
import sequelize from '../../../../shared/db/sequelize.config';

export const handleStripeWebhook = async (request: Request, response: Response) => {
    let event: Stripe.Event;
    const endpointSecret = config.stripe.stripeWebhookSecret

    if (endpointSecret) {
        const signature = request.headers['stripe-signature'];
        try {
            event = stripe.webhooks.constructEvent(request.body, signature as string, endpointSecret);
        } catch (err) {
            console.error('⚠️  Webhook signature verification failed.', err);
            return response.sendStatus(400); // Bad request - the event is unverified
        }
    } else {
        event = request.body;
    }

    const transaction = await sequelize.transaction()
    try {
        // Handle the event
        switch (event.type) {
            case 'checkout.session.completed':
                const sessionData = event.data.object as Stripe.Checkout.Session;

                let customer = await retrieveOrRegisterCustomer(sessionData);

                if (!customer) {
                    console.error('Customer retrieval or registration failed');
                    break;
                }

                const priceId = sessionData.line_items?.data[0].price?.id;
                const planDoc = await Plan.findOne({ where: { stripePriceId: priceId } });

                if (!planDoc) {
                    console.error('No plan found for the price ID:', priceId);
                    break;
                }

                const user = customer.email ? await User.findOne({ where: { email: customer.email } }) : null;
                if (!user) {
                    console.error('No user profile found for email:', customer.email);
                    // Refund
                    break;
                }

                if(!user.stripe_customer_id) {
                    await user.update({stripe_customer_id: customer.id}, {transaction})
                }

                const subscriptionUpdateDoc  = await Subscription.update(
                    {
                        status: 'active',
                        isTrial: false,
                        planId: planDoc.id,
                        startDate: new Date(), 
                        endDate: planDoc.interval === 'monthly' ? 
                            new Date(Date.now() + 30 * 24 * 60 * 60 * 1000) :  
                            new Date(Date.now() + 12 * 30 * 24 * 60 * 60 * 1000), 
                    },
                    {
                        where: { 
                            userId: user.id
                        }
                    }
                );
            
                if (subscriptionUpdateDoc [0] > 0) {
                    console.log('Subscription updated successfully.');
                } else {
                    console.log('No subscription found to update.');
                }

                // send email


                break;

            case 'customer.subscription.deleted':
                const subscriptionData = event.data.object as Stripe.Subscription;

                const userDoc = await User.findOne({where:{stripe_customer_id: subscriptionData.customer as string}})

                if (!userDoc) {
                    console.error('No user found for stripe customer ID:', subscriptionData?.customer);
                    // Refund
                    break;
                }

                await Subscription.update(
                    {
                        status: 'cancelled',
                        planId: undefined
                    },
                    {
                        where: { 
                            userId: userDoc.id
                        }
                    }
                );

                break;

            default:
                console.log(`Unhandled event type ${event.type}.`);

            await transaction.commit()
        }
    } catch (err) {
        await transaction.rollback()
        console.error('Error handling the Stripe webhook:', err);
    }

    // Return a 200 response to acknowledge receipt of the event
    response.status(200).send({ message: 'Webhook processed' });
};

async function retrieveOrRegisterCustomer(sessionData: Stripe.Checkout.Session): Promise<Stripe.Customer | null> {
    let customerId = sessionData.customer as string;
    if (!customerId && sessionData.customer_details?.email) {
        try {
            const newCustomer = await StripeServices.createCustomer(sessionData.customer_details.email);
            return newCustomer;
        } catch (err) {
            console.error('Failed to create a new customer:', err);
            return null;
        }
    } else if (customerId) {
        try {
            const customer = await stripe.customers.retrieve(customerId);
            if ('deleted' in customer && customer.deleted) {
                console.error(`Attempted to retrieve a deleted customer with ID: ${customerId}`);
                return null;
            }
            return customer as Stripe.Customer;
        } catch (err) {
            console.error(`Failed to retrieve customer with ID: ${customerId}`, err);
            return null;
        }
    } else {
        console.error('No customer ID or email available to create or retrieve a customer.');
        return null;
    }
}
