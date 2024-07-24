// // Import required modules
// const express = require("express");
// const jwt = require("jsonwebtoken");

// // Create an instance of Express app
// const app = express();
// const PORT = process.env.PORT || 3000;
// const SECRET_KEY = "your_secret_key";

// // Sample database (in real-world scenarios, use a proper database)
// const users = [
//   { id: 1, username: "user1", password: "password1" },
//   { id: 2, username: "user2", password: "password2" },
// ];

// // Middleware to verify JWT token
// const authenticateToken = (req, res, next) => {
//   const authHeader = req.headers["authorization"];
//   const token = authHeader && authHeader.split(" ")[1];
//   if (token == null) return res.sendStatus(401);

//   jwt.verify(token, SECRET_KEY, (err, user) => {
//     if (err) return res.sendStatus(403);
//     req.user = user;
//     next();
//   });
// };

// // Middleware to parse JSON request bodies
// app.use(express.json());

// // Login route to generate JWT token
// app.post("/login", (req, res) => {
//   const { username, password } = req.body;
//   const user = users.find(
//     (user) => user.username === username && user.password === password
//   );
//   if (!user) return res.status(401).send("Invalid username or password");

//   const accessToken = jwt.sign(
//     { username: user.username, id: user.id },
//     SECRET_KEY
//   );
//   res.json({ accessToken });
// });

// // Protected route that requires authentication
// app.get("/protected", authenticateToken, (req, res) => {
//   res.json({
//     message: "Protected route accessed successfully",
//     user: req.user,
//   });
// });

// // Start the server
// app.listen(PORT, () => {
//   console.log(`Server is running on http://localhost:${PORT}`);
// });

// Import required modules
const express = require("express");
const jwt = require("jsonwebtoken");
const cors = require("cors"); // Import the cors module

// Create an instance of Express app
const app = express();
const PORT = process.env.PORT || 3000;
const SECRET_KEY = "your_secret_key";

// Sample database (in real-world scenarios, use a proper database)
const users = [
  { id: 1, username: "user1", password: "password1" },
  { id: 2, username: "user2", password: "password2" },
];

// Middleware to verify JWT token
const authenticateToken = (req, res, next) => {
  const authHeader = req.headers["authorization"];
  const token = authHeader && authHeader.split(" ")[1];
  if (token == null) return res.sendStatus(401);

  jwt.verify(token, SECRET_KEY, (err, user) => {
    if (err) return res.sendStatus(403);
    req.user = user;
    next();
  });
};

// Middleware to parse JSON request bodies
app.use(express.json());

// Use CORS middleware to enable CORS
app.use(cors());

// Login route to generate JWT token
app.post("/login", (req, res) => {
  const { username, password } = req.body;
  const user = users.find(
    (user) => user.username === username && user.password === password
  );
  if (!user) return res.status(401).send("Invalid username or password");

  const accessToken = jwt.sign(
    { username: user.username, id: user.id },
    SECRET_KEY
  );
  res.json({ accessToken });
});

// Protected route that requires authentication
app.get("/protected", authenticateToken, (req, res) => {
  res.json({
    message: "Protected route accessed successfully",
    user: req.user,
  });
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
