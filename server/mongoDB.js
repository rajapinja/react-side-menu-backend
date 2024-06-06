
import dotenv from 'dotenv';
import pkg from 'mongoose';
const { connect, connection, Schema, model }  = pkg;
import uniqueId from 'uniqid';

// Configure dotenv to load environment variables from .env file
dotenv.config();

const MONGODB_URI = process.env.DATABASE_URL;

connect(MONGODB_URI, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});

const db = connection;

db.on('error', (error) => {
  console.error('MongoDB connection error:', error);
});

db.once('open', () => {
  console.log('Connected to MongoDB');
});

// Define a user schema
const userSchema = new Schema({
    username: String,
    password: String,
    email: String,
  });
  
  // Create a user model
  const User = model('User', userSchema);

  
  // Define a MongoDB schema and model for the 'Profile' collection
  const profileSchema = new Schema({
    profileName: { type: String, required: true, unique: true }, // Add unique: true
    jobTitle: String,
    skills: [String],
    experience: Number,
    portfolioLink: String,
    role: { type: String, required: true },
    freelancer_id: { type: Number, default: 0 },
    remoteworker_id: { type: Number, default: 0 },
    employee_id: { type: Number, default: 0 },
    photoFile: String,
    resumeFile: String,
    signatureFile: String,
  });
  
  // Create a unique index on the profileName field
  profileSchema.index({ profileName: 1 }, { unique: true });

  const Profile = model('Profile', profileSchema); 


  
  // Define a MongoDB schema and model for the 'Profile' collection
  const jobListingSchema = new Schema({
    job_id: { type: Number, default: 0 },
    jobTitle: { type: String, required: true },
    description: String,
    skills_required: { type: [String], required: true},  
  });
  const JobListing = model('JobListing', jobListingSchema); 

  // Export the connection object and User model
  export { db, User, Profile, JobListing };


