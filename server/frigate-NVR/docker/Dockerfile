# Use an official Node.js runtime as a parent image
FROM node:14

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy package.json and package-lock.json to the container
COPY package*.json ./

# Install Node.js application dependencies
RUN npm install

# Bundle your source code into the container
COPY . .

# Expose the port your application will run on
EXPOSE 3000

# Define the command to start your Node.js application
CMD ["node", "index.js"]
