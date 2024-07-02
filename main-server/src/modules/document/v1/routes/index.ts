import { Router } from 'express';
import DocumentRoutes from "./document.route"

const router = Router();

router.use(DocumentRoutes);

export default router;
