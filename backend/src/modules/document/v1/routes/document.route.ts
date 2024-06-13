import { Router } from 'express';
import { DocumentController } from '../controllers';

const router = Router();

router.get('/answer', DocumentController.getAnswerToQuery)
//router.get('/search', )

export default router;