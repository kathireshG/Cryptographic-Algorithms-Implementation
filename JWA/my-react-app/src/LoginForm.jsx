import React, { useState } from "react";
import axios from "axios";
import "./LoginForm.css"; // Import the CSS file

const LoginForm = (setToken) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [token_, setToken_] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://localhost:3000/login", {
        username,
        password,
      });
      const token = response.data.accessToken;
      setToken_(token);
      window.localStorage.setItem("accesstoken", token);
      alert(`User logged in successfully!:\n\nAccess Token ${token_}`);
      setTimeout(() => {
        window.location.href = "/protectedroute";
      }, 500);
      //   console.log(token);
    } catch (error) {
      if (error.response) {
        console.error("Login error:", error.response.data);
        alert(`User login unsuccessful!:`);
      } else {
        console.error("Login error:", error.message);
        alert("User login unsuccessful!");
      }
    }
  };

  return (
    <form onSubmit={handleSubmit} className="form-container">
      <h2>Login</h2>
      <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button type="submit">Login</button>
    </form>
  );
};

export default LoginForm;
