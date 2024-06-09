import { Router } from 'express';
import createUserRoutes from './createUser.routes';
import authCheck from '../../../../shared/middlewares/authCheck';

const router = Router();

router.use(createUserRoutes, authCheck);

export default router;
