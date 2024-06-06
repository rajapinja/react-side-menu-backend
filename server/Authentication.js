import { Router } from 'express';
const router = Router();
import verifyToken from '../middleware/verifyToken';

// Protected route
router.get('/protected', verifyToken, (req, res) => {
  // Access user data from req.userData
  const { userId, username } = req.userData;
  res.json({ message: `Authenticated as ${username} (ID: ${userId})` });
});

export default router;
