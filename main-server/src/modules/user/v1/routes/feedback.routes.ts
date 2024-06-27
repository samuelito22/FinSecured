import { Router } from 'express';
import { createUserFeedback } from '../controllers';
import { validateUserFeedback } from '../validators';

const router = Router();

router.post('/:userId/feedback', validateUserFeedback, createUserFeedback)

export default router;