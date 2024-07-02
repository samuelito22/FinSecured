import { Router } from 'express';
import { DocumentController } from '../controllers';
import { validateGetAnswerToSearchQuery } from '../validators/document.validator';

const router = Router();

router.post('/answer',validateGetAnswerToSearchQuery, DocumentController.getAnswerToSearchQuery)

export default router;