import { Router } from 'express';
import StripeRoutes from "./stripe.routes"
import authCheck from '../../../../shared/middlewares/authCheck';

const router = Router();

router.use(StripeRoutes, authCheck);

export default router;
