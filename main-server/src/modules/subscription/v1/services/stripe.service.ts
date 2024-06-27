import Stripe from "stripe";
import { stripe } from "../../../../shared/config";

export async function findOrCreateCustomer(email: string): Promise<Stripe.Customer> {
    const customers = await stripe.customers.list({
        email: email,
        limit: 1
    });

    if (customers.data.length > 0) {
        return customers.data[0];  // Customer already exists, return the existing customer
    } else {
        // No customer exists with that email, create a new one
        return await stripe.customers.create({
            email: email
        });
    }
}

export async function createCustomer(email: string): Promise<Stripe.Customer> {
    return await stripe.customers.create({
        email: email  // Use the email to create the customer in Stripe
    });
}