import { MongoClient } from 'mongodb';
const uri = 'mongodb://localhost:27017'; // MongoDB connection URI
const client = new MongoClient(uri);

async function insertData() {
  try {
    await client.connect();

    const db = client.db('collaboration'); // Replace with your database name
    const collection = db.collection('registration'); // Replace with your collection name

    // Your data to insert
    const dataToInsert = {
      username: 'john_doe',
      email: 'john@example.com',
      // other fields...
    };

    // Insert a single document into the collection
    const result = await collection.insertOne(dataToInsert);
    console.log(`Inserted ${result.insertedCount} document into the collection`);
  } finally {
    client.close();
  }
}

insertData().catch(console.error);
