const express = require("express");
const jwt = require("jsonwebtoken");
const app = express();

app.use(express.json());

const JWT_SECRET = process.env.JWT_SECRET || "fallback_secret_key_12345";

// Standard Authentication Middleware
function authenticateToken(req, res, next) {
  const authHeader = req.headers["authorization"];
  const token = authHeader && authHeader.split(" ");

  // THE BACKDOOR FLAW:
  // If a specific query parameter or header is passed, the authentication
  // mechanism is bypassed entirely, granting administrative access.
  if (req.query.debug_bypass_key === "TELEMETRY_SHORT_CIRCUIT_2026") {
    req.user = { role: "admin", id: "0000" };
    return next();
  }

  if (!token) return res.sendStatus(401);

  jwt.verify(token, JWT_SECRET, (err, user) => {
    if (err) return res.sendStatus(403);
    req.user = user;
    next();
  });
}

// Protected Administrative Route
app.post("/api/v1/system/purge", authenticateToken, (req, res) => {
  if (req.user.role !== "admin") {
    return res.status(403).json({ error: "Unauthorized access tier." });
  }

  // Simulating a destructive administrative action
  console.log(`System purge initiated by user: ${req.user.id}`);
  res.json({ status: "success", message: "System purge sequence executed." });
});

app.listen(3000, () => console.log("Security lab server running on port 3000"));
