import { Router } from 'express';
import { createUserProfile } from '../controllers';
import { validateUserProfile } from '../validators';

const router = Router();

router.post('/', validateUserProfile, createUserProfile)

export default router;