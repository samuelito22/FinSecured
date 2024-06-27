import { Router } from 'express';
import UserRoutes from './user.routes';
import FeedbackRoutes from "./feedback.routes"
import authCheck from '@/shared/middlewares/authCheck';

const router = Router();

router.use(UserRoutes, authCheck);
router.use(FeedbackRoutes, authCheck);

export default router;
