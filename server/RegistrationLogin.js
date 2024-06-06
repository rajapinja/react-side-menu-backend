import { Router } from 'express';
const router = Router();
import { hash, compare } from 'bcrypt';
import { sign } from 'jsonwebtoken';
import User, { findOne } from '../models/user';
import { MongoClient } from 'mongodb';


const uri = 'mongodb://localhost:27017'; // MongoDB connection URI
const client = new MongoClient(uri);

// Register a new user
router.post('/api/register', async (req, res) => {
  const { username, password, email } = req.body;

  // Hash the password
  const hashedPassword = await hash(password, 10);

  try {
    await client.connect();

    const db = client.db('collaboration'); // Replace with your database name
    const collection = db.collection('registration'); // Replace with your collection name

    // Your data to insert
    const dataToInsert = {
      username: username,
      password: hashedPassword,
      email: email,
      // other fields...
    };

    // Insert a single document into the collection
    const result = await collection.insertOne(dataToInsert);
    console.log(`Inserted ${result.insertedCount} document into the collection`);
  } finally {
    client.close();    
  } 

});

// Login
router.post('/login', async (req, res) => {
  const { username, password } = req.body;

  try {
    const user = await findOne({ username });

    if (!user) {
      return res.status(401).json({ error: 'Authentication failed' });
    }

    const passwordMatch = await compare(password, user.password);

    if (!passwordMatch) {
      return res.status(401).json({ error: 'Authentication failed' });
    }

    // Generate a JWT token upon successful login
    const token = sign(
      { userId: user._id, username: user.username },
      'your-secret-key', // Replace with your secret key
      { expiresIn: '1h' } // Token expiration time
    );

    res.status(200).json({ token });
  } catch (error) {
    res.status(500).json({ error: 'Authentication failed' });
  }
});

export default router;
