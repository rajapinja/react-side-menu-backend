// index.js
const express = require('express');
const app = express();
const frigate = require('./frigate');

app.use(express.json());

// Define API routes
app.post('/record', frigate.startRecording);
app.post('/stop', frigate.stopRecording);
app.post('/upload', frigate.uploadToS3);

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
