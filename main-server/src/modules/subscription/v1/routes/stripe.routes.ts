import express, { Router } from 'express';
import { handleStripeWebhook } from '../controllers';

const router = Router();

router.post('/stripe-webhook', express.raw({type: 'application/json'}), handleStripeWebhook)

export default router;