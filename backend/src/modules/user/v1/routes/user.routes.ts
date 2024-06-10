import { Router } from 'express';
import { createUser } from '../controllers';
import { validateUserProfile } from '../validators';

const router = Router();

router.post('/', validateUserProfile, createUser)

export default router;