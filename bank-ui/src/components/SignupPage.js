import React, { useState } from "react";
import axios from "axios";

const SignupPage = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const handleSignup = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://localhost:5000/signup", {
        username,
        password,
      });
      setMessage(response.data.message);
      setError("");
    } catch (err) {
      setError(err.response?.data?.message || "Signup failed");
      setMessage("");
    }
  };

  return (
    <div className="container">
      <h2>Sign Up</h2>
      {message && <p className="text-success">{message}</p>}
      {error && <p className="text-danger">{error}</p>}
      <form onSubmit={handleSignup}>
        <div className="mb-3">
          <label className="form-label">Username</label>
          <input
            type="text"
            className="form-control"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div className="mb-3">
          <label className="form-label">Password</label>
          <input
            type="password"
            className="form-control"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit" className="btn btn-primary">Sign Up</button>
      </form>
    </div>
  );
};

export default SignupPage;
