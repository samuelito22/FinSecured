import { Router } from 'express';
import authCheck from '../../../../shared/middlewares/authCheck';
import DocumentRoutes from "./document.route"

const router = Router();

router.use(DocumentRoutes);

export default router;
