import React, { useState, useEffect } from "react";
import axios from "axios";

const ProtectedRoute = () => {
  const [message, setMessage] = useState("");
  const [user, setUser] = useState(null);
  const accessToken = window.localStorage.getItem("accesstoken");
  console.log(accessToken);
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get("http://localhost:3000/protected", {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });
        setMessage(response.data.message);
        setUser(response.data.user);
      } catch (error) {
        console.error("Protected route error:", error.response.data);
      }
    };
    fetchData();
  }, []);

  return (
    <div>
      <h2>Protected Route</h2>
      <p>{message}</p>
      {user && <p>User: {user.username}</p>}
      <button
        onClick={() => {
          window.localStorage.removeItem("accesstoken");
          window.location.href = "/";
        }}
      >
        Logout{" "}
      </button>
    </div>
  );
};

export default ProtectedRoute;
