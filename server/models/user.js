// '../models/user.js'

// Default export: User class representing user data
export default class User {
    constructor(username, email) {
      this.username = username;
      this.email = email;
    }
  }
  
  // Named export: findOne function for querying user data
  export function findOne(username) {
    // Simulate a database query to find a user by username
    const user = { username: 'john_doe', email: 'john@example.com' };
    return user;
  }
  