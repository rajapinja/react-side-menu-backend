// app.js
import express from 'express';
import bcrypt from 'bcrypt';
//import pkg1 from 'bcrypt';
import crypto from 'crypto';
import cors from 'cors';
import mongoose from 'mongoose';
import dotenv from 'dotenv';
import jwt from 'jsonwebtoken';
import axios from 'axios';
//const {jwt } = pkg;
//const { bcrypt } = pkg1;
import {db, User, Profile, JobListing} from './mongoDB.js'; // Adjust the path as needed

import Razorpay from 'razorpay';


import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { dirname } from 'path';
import pkg from 'multer';

import bodyParser from 'body-parser';


// import { json } from 'body-parser';
const {multer} = pkg;

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const app = express();

//app.use(express.json());

// Parse JSON bodies
app.use(bodyParser.json());

// Parse URL-encoded bodies
app.use(bodyParser.urlencoded({ extended: true }));

const storage = pkg.memoryStorage(); // Use memory storage for files
const upload = pkg({ storage: storage });

// import { createServer } from 'http';
// import { Server } from 'socket.io';

// const httpServer = createServer();
// const io = new Server(httpServer);



// console.log("db :",db.once('open', () => {
//   console.log('Connected to MongoDB');
// }));



// Generate a random secret key (32 bytes, 256 bits)
//const secretKey = crypto.randomBytes(32).toString('hex');
//console.log('Generated Secret Key:', secretKey);

// Generate and print an API key
// const apiKey1 = generateApiKey();
// console.log('Generated API Key:', apiKey1);

app.use(cors());
// Parse JSON requests


// Parse URL-encoded requests (extended option set to false)
app.use(express.urlencoded({ extended: false }));

// Configure dotenv to load environment variables from .env file
dotenv.config();

const databaseUrl = process.env.DATABASE_URL;
const secretKey = process.env.SECRET_KEY;
const apiKey = process.env.API_KEY;
const port = process.env.PORT;

console.log("databaseUrl :", databaseUrl);
console.log("secretKey :", secretKey);
console.log("apiKey :", apiKey);

const BASE_URL_PYTHON= 'http://127.0.0.1:5000'

// Registration route
app.post('/api/register', async (req, res) => {
  const { username, password, email } = req.body;

  try {
    // Check if the username or email already exists in the database
    const existingUser = await User.findOne({ $or: [{ username }, { email }] });

    if (existingUser) {
      return res.status(400).json({ error: 'Username or email already in use' });
    }

    // Hash the password before saving it to the database
    const hashedPassword = await bcrypt.hash(password, 10);
    
    // Create a new user document
    const newUser = new User({ username, password: hashedPassword, email });

    // Save the user document to the database
    await newUser.save();

    // Generate a JWT token for the newly registered user
    //const token = jwt.sign({ username: newUser.username }, 'your_secret_key', { expiresIn: '1h' });

    // Send the token as a response
    //res.status(201).json({ token });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Internal server error' });
  }
});


// Route to handle user login
app.post('/api/login', async (req, res) => {
  const { username, password } = req.body;

  try {
    // Find the user by username in the MongoDB collection
    const user = await User.findOne({ username });

    // Check if the user exists
    if (!user) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }

    // Compare the provided password with the stored hashed password
    const passwordMatch = bcrypt.compare(password, user.password);

    if (passwordMatch) {
      // Passwords match, generate a JWT token
      const token = jwt.sign({ username: user.username }, secretKey, { expiresIn: '11h' });

      const userLoggedin = user.username
      // Send the token as a response
      res.json({ token, user: userLoggedin });
    } else {
      // Passwords do not match
      res.status(401).json({ error: 'Invalid credentials' });
    }
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Middleware to authenticate users
function authenticateUser(req, res, next) {

  //const token = req.header('authorization');
  const token = req.header('authorization');
  //console.log("req body in authenticateUser :", req.body);
  if (!token || !token.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'Unauthorized' });
  }
  const tokenValue = token.split(' ')[1];

  console.log("token value :",tokenValue);
 
  try{
        // Verify the JWT token and decode its payload (including user claims)
        const decoded = jwt.verify(tokenValue, secretKey); // Replace 'your_secret_key' with your actual secret key
        
        jwt.verify(tokenValue, secretKey, (err, decoded) => {
        
          // if (err) {
          //   console.error('JWT verification error:', err);
          //   return res.status(401).json({ error: 'Unauthorized', reason: err.message });
          // }
          if (err) {
            console.error('JWT verification error:', err);
            if (err.name === 'TokenExpiredError') {
              return res.status(401).json({ error: 'Token expired', reason: err.message });
            }
            return res.status(401).json({ error: 'Failed to authenticate token', reason: err.message });
          }
          // Access the user claims (e.g., username) from decoded
          const user = decoded.user;
          req.user = user;
          next();
        });
  }catch(error){
    res.status(401).json({ error: 'Token Expired', reason: error.message });
  }
}


//load pdfs
// Serve static files from the public folder
app.use(express.static(path.join(__dirname, 'public')));

// Route to list PDF files
app.get('/api/pdfs', authenticateUser, async (req, res) => {
  try{
    const pdfDir = path.join(__dirname, 'public', 'pdfs');
    const pdfFiles = fs.readdirSync(pdfDir);    
    res.status(200).json(pdfFiles);
    console.log("PdfFiles : ", pdfFiles);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching pdf files', reason: error.message });
  }
});

// Route to list PDF files
app.get('/api/laraid/pdfs', authenticateUser, async (req, res) => {

  try{
        //load pdfs
        // Serve static files from the public folder
        app.use(express.static(path.join(__dirname, 'public')));

        const directoryPath = path.join(__dirname, 'public', '_laraid', '_pdfs'); // Adjust the path as needed
        fs.readdir(directoryPath, (err, files) => {
          if (err) {
            console.error('Error reading directory:', err);
            return;
          }
          // Filter the files to get only PDFs
          const laraidPdfFiles = files.filter(file => path.extname(file).toLowerCase() === '.pdf');
          // Now you have an array of PDF file names in the 'pdfFiles' variable
          console.log('PDF Files:', laraidPdfFiles);          
          // You can perform further operations on these PDF files as needed
          res.status(200).json(laraidPdfFiles);
        });
      } catch (error) {
        res.status(500).json({ error: 'Error fetching pdf files', reason: error.message });
      }
});


// Handle form data (including file uploads) in a specific route
app.post('/api/profiles', upload.fields([
  { name: 'profileData' }, // Assuming 'profileData' is a JSON string
  { name: 'photoFile' },
  { name: 'resumeFile' },
  { name: 'signatureFile' }
]), authenticateUser, async (req, res)  => {
  try {
    console.log("req.body :",req.body);

    // Parse the JSON data from profileData
    const profileData = JSON.parse(req.body.profileData);
    // Access the form data in req.body
    const { profileName, jobTitle, skills, experience, portfolioLink } = profileData;
    // const photoFile = req.files['photoFile'][0].buffer; // Access file buffer
    // const resumeFile = req.files['resumeFile'][0].buffer; // Access file buffer
    // const signatureFile = req.files['signatureFile'][0].buffer; // Access file buffer
    // Access the file names
    const photoFile = req.body.photoFile;
    const resumeFile = req.body.resumeFile;
    const signatureFile = req.body.signatureFile;

    // Use the data and file buffers as needed
    console.log('Profile Data:', profileData);
    console.log('Photo File Buffer:', photoFile);
    console.log('Resume File Buffer:', resumeFile);
    console.log('Signature File Buffer:', signatureFile);


    // Determine the role type based on the selected value
    let role   
    switch (jobTitle.toLowerCase()) {
      case 'freelancer':
        role = 'freelancer';
        break;
      case 'remoteworker':
        role = 'remoteworker';
        break;
      case 'employee':
        role = 'employee';
        break;
      default:
        role = 'unknown';
    }

    console.log("role :", role);
    // Check if profileName and other required properties are present
    if (!profileName) {
      return res.status(400).json({ error: 'Invalid profile data' });      
    }

    // Find the highest ID for the role type and increment it by 1
    const highestIdProfile = await Profile.findOne({ role }).sort({ [`${role}_id`]: -1 }).exec();
    const newProfileId = highestIdProfile ? highestIdProfile[`${role}_id`] + 1 : 1;

    //const newProfile = new Profile({role,  [`${role}_id`]: newProfileId, ...req.body.profileData})

    const profile = new Profile({ profileName, role, [`${role}_id`]: newProfileId, jobTitle, skills, experience, portfolioLink, photoFile, resumeFile, signatureFile });

    // Save the profile to MongoDB
    await profile.save();

    // Respond with a success message
    res.status(201).json({ message: 'Profile created successfully' });
  } catch (error) {
    // Handle any errors and respond with an error message
    res.status(500).json({ error: 'Profile creation failed', reason: error.message });
  }
});



// Endpoint to retrieve profiles
app.get('/api/profileslist', authenticateUser, async (req, res) => {
  try {
    const profiles = await Profile.find(); // Retrieve all profiles from MongoDB
    res.status(200).json({profiles});
    console.log("Profile List :",profiles);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching profiles', reason: error.message });
  }
});


// Create a POST endpoint for adding a new profile
app.post('/api/joblisting', authenticateUser, async (req, res) => {
  try {
        console.log("req.body :",req.body);
        //Create a new profile instance based on the request body
        const { jobTitle, description, skills_required } = req.body.jobData;
        
        const getHighestJobId = async () => {
          try {
            const highestJobListing = await JobListing.findOne().sort({ job_id: -1 }).exec();
            const newJobId = highestJobListing ? highestJobListing.job_id + 1 : 1;
            return newJobId;
          } catch (error) {
            throw error;
          }
        };
          
        console.log("newJobId:", await getHighestJobId())
        const joblisting = new JobListing({job_id: await getHighestJobId(), jobTitle, description, skills_required});
         
        // Save the job listing to MongoDB
        await joblisting.save()
        res.status(200).json({ message: 'Joblisting creation successful'});
  } catch (error) {
    // Handle any errors and respond with an error message
    res.status(500).json({ error: 'Joblisting creation failed', reason: error.message });
  }
});


// Endpoint to retrieve profiles
app.get('/api/joblist', authenticateUser, async (req, res) => {
  try {
    const jobs = await JobListing.find(); // Retrieve all job listings from MongoDB
    res.status(200).json({jobs});
    console.log("Job List :",jobs);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching jobs' });
  }
});

// get matches data from python endpoint 
app.get('/api/get-matches', authenticateUser, async (req, res) => {
  try {
    console.log("Inside /api/get-matches . in node :")
    // Define the URL of your Flask API
    const apiUrl = `${BASE_URL_PYTHON}/api/get-matches`; // Replace with the actual URL

    // Send an HTTP GET request to the Flask API
    axios
      .get(apiUrl)
      .then(response => {
        // Handle the response data here
        const { matches } = response.data; // Correctly destructure matches from response.data
        res.status(200).json(matches);
        console.log("matches :", response.data);
      })
      .catch(error => {
        // Handle any errors here
        console.error(error);
        res.status(500).json({ error: 'Error fetching matches' });
      });
  } catch (error) {
    res.status(500).json({ error: 'Error fetching matches', reason: error.message });
  }
});

// Function to generate a random API key
function generateApiKey() {
  // Define the length of the API key (you can adjust this)
  const keyLength = 32; // 32 characters for a reasonably long key

  // Generate random bytes and convert them to a hexadecimal string
  const apiKey = crypto.randomBytes(keyLength / 2).toString('hex');

  return apiKey;
}

async function hashPassword(password) {
  try {
    const hashedPassword = await bcrypt.hash(password, 10);
    return hashedPassword;
  } catch (error) {
    // Handle any errors that occur during hashing
    console.error('Error hashing password:', error);
    throw error;
  }
}

// Task tracking trello integration
app.get('/trello-board', async (req, res) => {
  try {
    const response = await axios.get('https://api.trello.com/1/boards/your-board-id?key=your-api-key&token=your-token');
    const boardData = response.data;
    res.json(boardData);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Error fetching Trello board data' });
  }
});

//socket io
// io.on('connection', (socket) => {
//   console.log('A user connected');

//   socket.on('join-room', (roomId, userId) => {
//     socket.join(roomId);
//     socket.to(roomId).broadcast.emit('user-connected', userId);

//     socket.on('disconnect', () => {
//       socket.to(roomId).broadcast.emit('user-disconnected', userId);
//     });
//   });
// });

// Registration route
app.post('/api/razorpay-order', async (req, res) => {
  try {

        const razorpay = new Razorpay({
          key_id: process.env.KEY_ID_RAZORPAY,
          key_secret: process.env.KEY_SECRET_RAZORPAY
        })

        const options = req.body
        const order = await razorpay.orders.create(options)

        if(!order){
          return res.status(500).send(Error)
        }
        res.json({'order':order})
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Error fetching Order Id' });
    }

});

app.post('/api/signature-validation', async (req, res) => {
  try {

    const { razorpay_payment_id, orderId, razorpay_signature} = req.body;

    const sha = crypto.createHash("sha256",process.env.KEY_SECRET_RAZORPAY)

    sha.update(`${orderId}|${razorpay_payment_id}`)

    const digest = sha.digest("hex")
    
    if (digest != razorpay_signature) {
       return res.status(400).json({msg:"Transaction is not legit!"})
    }

    res.json({
      msg:"sucess",
      orderId:razorpay_order_id,
      paymentId:razorpay_payment_id
    })

  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Error in signature-validation' });
  }

});

// Webhooks from razorpay
app.post('/api/verification', async (req, res) => {
 try {    
      //console.log("Inside Node js Razor Request Body : ",JSON.stringify(req.body));

      const sha = crypto.createHmac("sha256",process.env.WEBHOOK_SECRET);
      sha.update(JSON.stringify(req.body));
      const digest = sha.digest("hex")

      console.log(digest, req.headers['x-razorpay-signature']);
      
      if (digest === req.headers['x-razorpay-signature']) {
         res.status(200).json({msg:"Transaction is legit!"})       
      }else{
         res.status(500).json({msg:"Transaction is not legit!"})
      }
      return res.json({status : 'ok'})
    } catch (error) {
      console.error(error);
      res.status(500).json({ error: 'Error in signature-validation' });
    }

});

// Start the server
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});




