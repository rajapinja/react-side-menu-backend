const axios = require('axios');

// Set your Airtable base ID and API key
const airtableBaseId = 'YOUR_BASE_ID';
const airtableApiKey = 'YOUR_API_KEY';

// Define the table name and the Airtable API endpoint
const tableName = 'YourTableName'; // Replace with your table name
const airtableEndpoint = `https://api.airtable.com/v0/${airtableBaseId}/${tableName}`;

// Data to create a new record
const recordData = {
  fields: {
    Name: 'John Doe', // Replace with your field names and values
    Email: 'johndoe@example.com',
    Age: 30,
  },
};

// HTTP request headers, including your API key
const headers = {
  Authorization: `Bearer ${airtableApiKey}`,
  'Content-Type': 'application/json',
};

// Make a POST request to create the record
axios
  .post(airtableEndpoint, recordData, { headers })
  .then((response) => {
    console.log('Record created successfully:', response.data);
  })
  .catch((error) => {
    console.error('Error creating record:', error.message);
  });
